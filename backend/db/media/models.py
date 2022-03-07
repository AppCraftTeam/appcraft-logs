from django.db import models

from backend.db.models import BaseModel


class BaseImageModel(BaseModel):
    file = models.ImageField(verbose_name='image')

    def __str__(self):
        return self.file.name

    class Meta:
        abstract = True


class BaseAudioModel(BaseModel):
    file = models.FileField(verbose_name='audio')

    def __str__(self):
        return self.file.name

    class Meta:
        abstract = True
