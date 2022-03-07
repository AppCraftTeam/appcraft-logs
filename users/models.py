from django.db import models

from backend.db.models import BaseUserModel

from users.validators import validate_phone_number


class UserModel(BaseUserModel):
    class Genders(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    phone = models.CharField(max_length=14, validators=[validate_phone_number])
    birth_date = models.DateField()
    gender = models.IntegerField(choices=Genders.choices)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'app__users_list'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
