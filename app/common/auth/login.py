from app.common.library import cognito


def login(username, password):
    client = cognito.create_client()

    resp, msg = cognito.idp_admin_initiate_auth(client, username, password)

    if msg is not None:
        return {"message": msg, "error": True, "success": False, "data": None}

    if resp.get("AuthenticationResult"):
        return {
            "message": "success",
            "error": False,
            "success": True,
            "data": {
                "id_token": resp["AuthenticationResult"]["IdToken"],
                "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                "token_type": resp["AuthenticationResult"]["TokenType"],
            },
        }

    # this code block is relevant only when MFA is enabled
    return {"error": True, "success": False, "data": None, "message": None}
