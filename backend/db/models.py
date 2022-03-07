from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoDefaultUserManager
from django.db import models
from django.utils import timezone

from backend.db.enums import RecordTypes
from backend.db.managers import Manager, UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)

    default_manager = models.Manager()

    objects = Manager(records_type=RecordTypes.ANY)
    available = Manager(records_type=RecordTypes.AVAILABLE)
    unavailable = Manager(records_type=RecordTypes.UNAVAILABLE)

    @property
    def is_available(self):
        return not bool(self.deleted_at)

    def restore(self):
        self.deleted_at = None
        self.save()
        return self

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
        return self

    class Meta:
        abstract = True


class BaseUserModel(AbstractUser, SoftDeleteModel):
    first_name = None
    last_name = None
    last_login = None
    date_joined = None

    # default manager.
    # shouldn't be used by project developers as it doesn't support soft-delete feature.
    default_manager = DjangoDefaultUserManager()

    objects = UserManager(records_type=RecordTypes.ANY)
    available = UserManager(records_type=RecordTypes.AVAILABLE)
    unavailable = UserManager(records_type=RecordTypes.UNAVAILABLE)

    def delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()
        return self

    def restore(self):
        self.deleted_at = None
        self.is_active = True
        self.save()
        return self

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    def save(self, *args, **kwargs):
        self.id = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    class Meta:
        abstract = True
