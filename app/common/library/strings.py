from django import forms
from django.core.validators import validate_email, URLValidator  # EmailValidator
from django.core.exceptions import ValidationError


def check_if_email(input_string):
    if input_string is None:
        return False

    try:
        # validate_email = EmailValidator()
        validate_email(input_string.strip())

        return True
    except ValidationError:
        return False


def check_if_url(input_string):
    if input_string is None:
        return False

    try:
        validate_url = URLValidator()
        validate_url(input_string.strip())

        return True
    except ValidationError:
        return False


def sanitize_email(input_string):
    if input_string is None:
        return None

    form_field = forms.EmailField()
    return form_field.clean(input_string).strip()


def sanitize_url(input_string):
    if input_string is None:
        return None

    form_field = forms.URLField()
    return form_field.clean(input_string).strip()


def sanitize_phone(input_string):
    if input_string is None:
        return None

    return input_string.strip()
