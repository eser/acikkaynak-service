import graphene
from app.common.auth.signup_confirm import signup_confirm


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class SignupConfirmResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()


class SignupConfirmMutation(graphene.Mutation):
    Output = SignupConfirmResponse

    class Arguments:
        username = graphene.String(required=True)
        confirmation_code = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = signup_confirm(kwargs["username"], kwargs["confirmation_code"])

        if not resp["success"]:
            return SignupConfirmResponse(is_successful=False, error=resp["message"])

        return SignupConfirmResponse(
            is_successful=True,
            error=None,
        )


class Mutation(graphene.ObjectType):
    signup_confirm = SignupConfirmMutation.Field()
