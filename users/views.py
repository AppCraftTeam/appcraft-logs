from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import MyProfileSerializer


class MyProfileView(RetrieveAPIView):
    serializer_class = MyProfileSerializer
    # loggable_http_methods = '__all__'

    def get_object(self):
        return self.request.user


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def my_profile_fbv(request):
    return Response()
my_profile_fbv.loggable_http_methods = []  # noqa
