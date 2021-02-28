from app.common.library import cognito, strings


def get_user_by(field, value):
    client = cognito.create_client()

    value_quoted = value.replace('"', '\\"')
    filter_string = f'{field} = "{value_quoted}"'

    resp, msg = cognito.idp_list_users(client, filter_string)

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    if len(resp["Users"]) == 0:
        return {"message": "success", "error": False, "success": True, "data": None}

    return {
        "message": "success",
        "error": False,
        "success": True,
        "data": resp["Users"][0],
    }


def get_user(login):
    if strings.check_if_email(login):
        return "email", get_user_by("email", strings.sanitize_email(login))

    return "phone", get_user_by("phone_number", strings.sanitize_phone(login))
