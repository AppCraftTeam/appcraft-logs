import random
import string
from datetime import datetime

from django.utils.timezone import make_aware
from pytils.translit import slugify


def to_milliseconds(dt: datetime):
    epoch = make_aware(datetime.utcfromtimestamp(0))

    try:
        dt = make_aware(dt)
    except ValueError:
        pass

    return int((dt - epoch).total_seconds() * 1000.0)


def to_datetime(milliseconds: int):
    return make_aware(datetime.utcfromtimestamp(int(milliseconds) / 1000.0))


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def clear_file_name(name):
    exs = name.split('.')[-1]
    exs = exs.lower()
    exs = f'.{exs}'

    new_name = name.rstrip(exs)

    return slugify(new_name) + exs
