import re
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError


def phone_number_validator(value):
    if not bool(re.match(r'^\d{12}$', value)):
        raise ValidationError(_("Not a valid phone number"))

    return value
