import phonenumbers

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    try:
        phone_instance = phonenumbers.parse(value)
    except Exception as ex:
        raise ValidationError(ex)

    if not phonenumbers.is_valid_number(phone_instance):
        raise ValidationError('phone is not valid')
