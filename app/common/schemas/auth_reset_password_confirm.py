import graphene
from app.common.auth.reset_password_confirm import reset_password_confirm


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class ResetPasswordConfirmResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()


class ResetPasswordConfirmMutation(graphene.Mutation):
    Output = ResetPasswordConfirmResponse

    class Arguments:
        username = graphene.String(required=True)
        confirmation_code = graphene.String(required=True)
        new_password = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = reset_password_confirm(
            kwargs["username"], kwargs["confirmation_code"], kwargs["new_password"]
        )

        if not resp["success"]:
            return ResetPasswordConfirmResponse(
                is_successful=False, error=resp["message"]
            )

        return ResetPasswordConfirmResponse(
            is_successful=True,
            error=None,
        )


class Mutation(graphene.ObjectType):
    reset_password_confirm = ResetPasswordConfirmMutation.Field()
