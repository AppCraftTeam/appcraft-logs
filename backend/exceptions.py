from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class HTTPException(APIException):
    def __init__(self, reason, status_code):
        self.detail = reason
        self.status_code = status_code


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Request data is invalid.')


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Entity not found.')
