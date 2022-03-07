import json
from uuid import uuid4

from django.urls import resolve
from django.utils import timezone

from .apps import AppcraftLoggingConfig as LogsConfig
from .clickhouse.models import LogModel
from .utils import clear_file_name, to_milliseconds


class LogsMiddleware:
    ALL = '__all__'
    FBV_NAME = 'WrappedAPIView'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.__is_loggable(request):
            return self.get_response(request)

        log = LogModel(
            uuid=uuid4(),
            time=to_milliseconds(timezone.now()),
            start_at=timezone.now(),
            method=request.method,
            url=request.path,
            headers=str(request.headers),
            query_params=str(request.GET),
        )

        if (
            hasattr(request, 'body') and
            len(request.body) > 0 and
            request.content_type != 'multipart/form-data'
        ):
            log.request_body = json.loads(request.body)
        if request.content_type == 'multipart/form-data':
            file_names = self.__extract_file_names(request)
            log.request_body = ', '.join(file_names)
        else:
            log.request_body = ''

        response = self.get_response(request)

        if not request.user.is_anonymous:
            log.user_id = request.user.id

        log.response_body = str(response.data) if hasattr(response, 'data') else ''
        log.status_code = response.status_code
        log.error_reason = response.status_text if hasattr(response, 'status_text') else ''

        LogsConfig.db.insert([log])

        return response

    def __is_loggable(self, request):
        if request.path.find('api') == -1:
            return False

        if self.__is_fbv(request):
            view = resolve(request.path).func
        else:
            view = resolve(request.path).func.view_class

        try:
            if type(view.loggable_http_methods) != list:
                return True
            return request.method in [i.upper() for i in view.loggable_http_methods]
        except AttributeError:
            # loggable by default
            return True

    def __extract_file_names(self, request):
        file_names = []
        for key in request.FILES:
            files_list = request.FILES.getlist(key)
            file_names += [clear_file_name(file.name) for file in files_list]
        return file_names

    def __is_fbv(self, request):
        match = resolve(request.path).func
        # in case of fbv, match.__qualname__ will contain string 'WrappedAPIView'
        # in case of cbv, match.__qualname__ will contain view name
        return match.__qualname__ == self.FBV_NAME
