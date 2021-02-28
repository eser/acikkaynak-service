import graphene

from app.common.auth.login import login
from app.common.auth.tokens import decode_token
from app.profiles.schemas.queries import ProfileNode
from app.profiles.actions.get_profiles_by_user import get_profiles_by_user


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class LoginResponseDetails(graphene.ObjectType):
    id_token = graphene.Boolean()
    refresh_token = graphene.String()
    access_token = graphene.String()
    expires_in = graphene.Int()
    token_type = graphene.String()


class LoginResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()
    details = graphene.Field(LoginResponseDetails)
    profiles = graphene.List(ProfileNode)


class LoginMutation(graphene.Mutation):
    Output = LoginResponse

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = login(kwargs["username"], kwargs["password"])

        if not resp["success"]:
            return LoginResponse(
                is_successful=False, error=resp["message"], details=None, profiles=None
            )

        user_jwt = decode_token(resp["data"]["access_token"])

        profiles = get_profiles_by_user(user_jwt["username"])

        return LoginResponse(
            is_successful=True,
            error=None,
            details=LoginResponseDetails(
                id_token=resp["data"]["id_token"],
                refresh_token=resp["data"]["refresh_token"],
                access_token=resp["data"]["access_token"],
                expires_in=resp["data"]["expires_in"],
                token_type=resp["data"]["token_type"],
            ),
            profiles=profiles,
        )


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
