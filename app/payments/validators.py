import re
from django.core.exceptions import ValidationError


def deadline_validator(value):
    if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', value):
        return ValidationError(f"{value} is not a valid deadline for card")

    return value
