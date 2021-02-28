import graphene
from app.common.auth.get_user import get_user


# queries


class CheckUserResponse(graphene.ObjectType):
    user_exists = graphene.Boolean()
    username = graphene.String()
    status = graphene.String()


class Query(graphene.ObjectType):
    check_user = graphene.Field(CheckUserResponse, login=graphene.String(required=True))

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_check_user(parent, info, login):
        # pylint:disable=unused-variable
        login_type, resp = get_user(login)

        if resp["data"] is None:
            return CheckUserResponse(
                user_exists=False, username=None, status="NOT_FOUND"
            )

        if not resp["data"]["Enabled"]:
            return CheckUserResponse(
                user_exists=True, username=resp["data"]["Username"], status="DISABLED"
            )

        return CheckUserResponse(
            user_exists=True,
            username=resp["data"]["Username"],
            status=resp["data"]["UserStatus"],
        )


# mutations


class Mutation(graphene.ObjectType):
    pass
