from rest_framework import serializers

from users.models import UserModel


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
