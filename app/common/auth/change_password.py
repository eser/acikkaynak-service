from app.common.library import cognito
from app.common.auth.tokens import decode_token
from app.common.models import User


def change_password(access_token, previous_password, proposed_password):
    user_jwt = decode_token(access_token)

    client = cognito.create_client()

    # pylint:disable=unused-variable
    resp, msg = cognito.idp_change_password(
        client, access_token, previous_password, proposed_password
    )

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    user = User.objects.get(username=user_jwt["username"])
    user.set_password(proposed_password)
    user.save()

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": None,
    }
