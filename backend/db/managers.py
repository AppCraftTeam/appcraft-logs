from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models.manager import BaseManager as DjangoBaseManager

from backend.db.enums import RecordTypes
from backend.db.query import BaseQuerySet, UserQuerySet


class Manager(DjangoBaseManager.from_queryset(BaseQuerySet)):
    def __init__(self, records_type: RecordTypes = None, *args, **kwargs):
        super().__init__()
        self.records_type = records_type
        self._queryset_class = BaseQuerySet

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted_at__isnull=True)


class UserManager(DjangoUserManager, DjangoBaseManager.from_queryset(UserQuerySet)):
    def __init__(self, records_type: RecordTypes = None, *args, **kwargs):
        super().__init__()
        self.records_type = records_type
        self._queryset_class = UserQuerySet

    def get_queryset(self, *args, **kwargs):
        if self.records_type in [RecordTypes.ANY, None]:
            return super().get_queryset(*args, **kwargs)
        elif self.records_type == RecordTypes.AVAILABLE:
            return super().get_queryset(*args, **kwargs).filter(deleted_at__isnull=True, is_active=True)
        elif self.records_type == RecordTypes.UNAVAILABLE:
            return super().get_queryset(*args, **kwargs).filter(deleted_at__isnull=False, is_active=False)
        else:  # wtf?
            return super().get_queryset(*args, **kwargs).none()
