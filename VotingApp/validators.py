from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_fl_name(value):
    if len(value.split(' ')) != 2:
        raise ValidationError(
            _('%(value)s is not a correct pair of first and last name'),
            params={'value': value},
        )
