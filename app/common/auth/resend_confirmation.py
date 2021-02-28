from app.common.library import cognito


def resend_confirmation(username):
    client = cognito.create_client()

    # pylint:disable=unused-variable
    resp, msg = cognito.idp_resend_confirmation_code(client, username)

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": None,
    }
