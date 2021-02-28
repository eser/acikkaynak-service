import hmac
import hashlib
import base64
import boto3
from django.conf import settings


def get_secret_hash(username):
    msg = username + settings.AWS["COGNITO_CLIENT_ID"]
    dig = hmac.new(
        str(settings.AWS["COGNITO_CLIENT_SECRET"]).encode("utf-8"),
        msg=str(msg).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    secret_hash = base64.b64encode(dig).decode()

    return secret_hash


def create_client():
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=settings.AWS["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=settings.AWS["AWS_SECRET_ACCESS_KEY"],
        region_name=settings.AWS["AWS_DEFAULT_REGION"],
    )

    return client


def idp_list_users(client, filter_string):
    try:
        resp = client.list_users(
            UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            Filter=filter_string,
        )
    except client.exceptions.InvalidParameterException:
        return None, "Invalid parameter"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_admin_initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)

    try:
        resp = client.admin_initiate_auth(
            UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,
            },
            ClientMetadata={
                "username": username,
                "password": password,
            },
        )
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_sign_up(client, username, password, user_attributes):
    secret_hash = get_secret_hash(username)

    try:
        resp = client.sign_up(
            # UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            SecretHash=secret_hash,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": key, "Value": str(value)}
                for key, value in user_attributes.items()
            ],
        )
    except client.exceptions.UsernameExistsException:
        return None, "This username already exists"
    except client.exceptions.InvalidPasswordException:
        return None, "Password should have Caps, Special chars, Numbers"
    except client.exceptions.UserLambdaValidationException:
        return None, "Email already exists"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_confirm_sign_up(client, username, confirmation_code):
    secret_hash = get_secret_hash(username)

    try:
        resp = client.confirm_sign_up(
            # UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            SecretHash=secret_hash,
            Username=username,
            ConfirmationCode=confirmation_code,
            ForceAliasCreation=False,
        )
    except client.exceptions.UserNotFoundException:
        return None, "Username doesn't exist"
    except client.exceptions.CodeMismatchException:
        return None, "Invalid verification code"
    except client.exceptions.NotAuthorizedException:
        return None, "User is already confirmed"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_forgot_password(client, username):
    secret_hash = get_secret_hash(username)

    # Parameter validation failed: Unknown parameter in input: "UserPoolId", must be
    # one of: ClientId, SecretHash, UserContextData, Username,
    # AnalyticsMetadata, ClientMetadata
    try:
        resp = client.forgot_password(
            # UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            SecretHash=secret_hash,
            Username=username,
        )
    except client.exceptions.UserNotFoundException:
        return None, "Username doesn't exist"
    except client.exceptions.InvalidParameterException:
        return None, "User is not confirmed yet"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_confirm_forgot_password(client, username, confirmation_code, new_password):
    secret_hash = get_secret_hash(username)

    try:
        resp = client.confirm_forgot_password(
            # UserPoolId=settings.AWS["COGNITO_USER_POOL_ID"],
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            SecretHash=secret_hash,
            Username=username,
            ConfirmationCode=confirmation_code,
            Password=new_password,
        )
    except client.exceptions.UserNotFoundException:
        return None, "Username doesn't exist"
    except client.exceptions.CodeMismatchException:
        return None, "Invalid verification code"
    except client.exceptions.InvalidParameterException:
        return None, "User is not confirmed yet"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_resend_confirmation_code(client, username):
    secret_hash = get_secret_hash(username)

    try:
        resp = client.resend_confirmation_code(
            ClientId=settings.AWS["COGNITO_CLIENT_ID"],
            SecretHash=secret_hash,
            Username=username,
        )
    except client.exceptions.UserNotFoundException:
        return None, "Username doesn't exist"
    except client.exceptions.InvalidParameterException:
        return None, "User is already confirmed"
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None


def idp_change_password(client, access_token, previous_password, proposed_password):
    try:
        resp = client.change_password(
            AccessToken=access_token,
            PreviousPassword=previous_password,
            ProposedPassword=proposed_password,
        )
    except Exception as exc:  # pylint:disable=broad-except
        return None, exc.__str__()

    return resp, None
