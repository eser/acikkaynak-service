import jwt


def decode_token(access_token):
    access_token_jwt = jwt.decode(
        access_token,
        # TODO will be enabled
        options={"verify_signature": False},
    )

    # checked key named "sub" due to verification of
    # jwt token's validity
    if not access_token_jwt.get("sub"):
        raise ValueError("Token is invalid")

    return access_token_jwt
