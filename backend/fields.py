from rest_framework import serializers

from backend.utils import to_datetime, to_milliseconds


class DateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return to_milliseconds(value)

    def to_internal_value(self, value):
        return to_datetime(int(value))
