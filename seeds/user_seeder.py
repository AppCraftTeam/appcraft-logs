import os

from django.contrib.auth.hashers import make_password
from django.utils import timezone

from users.models import UserModel


class UserSeeder:
    def create(self):
        self.create_superuser()

    def create_superuser(self):
        UserModel.objects.get_or_create(
            username=os.getenv('ROOT_USERNAME', 'admin'),
            defaults={
                'fname': 'admin',
                'lname': 'admin',
                'birth_date': timezone.now(),
                'gender': UserModel.Genders.MALE,
                'phone': '+76666666666',
                'email': 'superadmin@admin.com',
                'is_superuser': True,
                'is_staff': True,
                'password': make_password(os.getenv('ROOT_PASSWORD', 'admin'))
            }
        )
    print('Superuser seeded seccessfull! [OK]')
