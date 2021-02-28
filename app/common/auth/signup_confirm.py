from django.utils.text import slugify
from app.common.library import cognito
from app.common.models import User


def signup_confirm(username, confirmation_code):
    client = cognito.create_client()

    # pylint:disable=unused-variable
    resp, msg = cognito.idp_confirm_sign_up(client, username, confirmation_code)

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    user = User.objects.get(username=username)
    user.is_active = True

    slug = slugify(f"{user.first_name} {user.last_name}")

    # profile =
    user.profiles.create(
        slug=slug,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        birthdate=user.birthdate,
        email=user.email,
        phone=user.phone,
        profile_picture_uri=user.profile_picture_uri,
        # timezone="Europe/Berlin",
    )

    user.save()

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": None,
    }
