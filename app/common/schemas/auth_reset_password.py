import graphene
from app.common.auth.reset_password import reset_password


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class ResetPasswordResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()


class ResetPasswordMutation(graphene.Mutation):
    Output = ResetPasswordResponse

    class Arguments:
        username = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = reset_password(kwargs["username"])

        if not resp["success"]:
            return ResetPasswordResponse(is_successful=False, error=resp["message"])

        return ResetPasswordResponse(
            is_successful=True,
            error=None,
        )


class Mutation(graphene.ObjectType):
    reset_password = ResetPasswordMutation.Field()
