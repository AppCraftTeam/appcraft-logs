from django.db import models
from django.utils import timezone


class BaseQuerySet(models.QuerySet):
    def restore(self):
        self.update(deleted_at=None)
        return self

    def soft_delete(self):
        self.update(deleted_at=timezone.now())
        return self


class UserQuerySet(BaseQuerySet):
    def restore(self):
        self.update(deleted_at=None, is_active=True)
        return self

    def soft_delete(self):
        self.update(deleted_at=timezone.now())
        return self
