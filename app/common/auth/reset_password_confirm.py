from app.common.library import cognito
from app.common.models import User


def reset_password_confirm(username, confirmation_code, new_password):
    client = cognito.create_client()

    # pylint:disable=unused-variable
    resp, msg = cognito.idp_confirm_forgot_password(
        client, username, confirmation_code, new_password
    )

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    user = User.objects.get(username=username)
    user.is_active = True
    user.set_password(new_password)
    user.save()

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": None,
    }
