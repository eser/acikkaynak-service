# from time import time
from django.conf import settings

from app.common.library import cognito, dicts, strings
from app.common.models import User


def signup(
    login,
    password,
    first_name=None,
    last_name=None,
    gender=None,
    birthdate=None,
    email=None,
    phone=None,
    profile_picture_uri=None,
    locale=None,
):
    login_is_email = strings.check_if_email(login)
    email_sanitized = strings.sanitize_email(login if login_is_email else email)
    phone_sanitized = strings.sanitize_phone(phone if login_is_email else login)
    login_sanitized = email_sanitized if login_is_email else phone_sanitized
    profile_picture_uri_sanitized = strings.sanitize_url(profile_picture_uri)

    if login_is_email:
        if "email" not in settings.LOGIN_OPTIONS:
            return {
                "message": "login by e-mail is disabled",
                "error": True,
                "success": False,
                "data": None,
            }
        if email is not None:
            return {
                "message": f"both {login_sanitized} and {email_sanitized} is specified as e-mail",
                "error": True,
                "success": False,
                "data": None,
            }
    else:
        if "phone" not in settings.LOGIN_OPTIONS:
            return {
                "message": "login by phone is disabled",
                "error": True,
                "success": False,
                "data": None,
            }
        if phone is not None:
            return {
                "message": f"both {login_sanitized} and {phone_sanitized} is specified as phone number",
                "error": True,
                "success": False,
                "data": None,
            }

    # now = time()

    client = cognito.create_client()

    user_attributes = dicts.create_dict_for_attributes(
        given_name=first_name,
        family_name=last_name,
        gender=gender,
        birthdate=birthdate,
        email=email_sanitized,
        phone_number=phone_sanitized,
        picture=profile_picture_uri_sanitized,
        locale=locale,
        # TODO re-enable later
        # updated_at=now,
    )

    resp, msg = cognito.idp_sign_up(client, login_sanitized, password, user_attributes)

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    if not resp.get("CodeDeliveryDetails"):
        # this code block is relevant only when MFA is enabled
        return {"error": True, "success": False, "data": None, "message": None}

    user_uuid = resp["UserSub"]

    # created_user =
    User.objects.create_user(
        user_uuid,
        password=password,
        is_active=False,
        username=user_uuid,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthdate=birthdate,
        email=login_sanitized,
        phone=phone_sanitized,
        profile_picture_uri=profile_picture_uri_sanitized,
        locale=locale,
    )

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": {
            "code_delivery_details": {
                "attribute_name": resp["CodeDeliveryDetails"]["AttributeName"],
                "delivery_medium": resp["CodeDeliveryDetails"]["DeliveryMedium"],
                "destination": resp["CodeDeliveryDetails"]["Destination"],
            },
            "user_confirmed": resp["UserConfirmed"],
            "user_sub": resp["UserSub"],
        },
    }
