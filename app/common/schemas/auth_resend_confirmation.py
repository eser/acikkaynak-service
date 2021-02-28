import graphene
from app.common.auth.resend_confirmation import resend_confirmation


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class ResendConfirmationResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()


class ResendConfirmationMutation(graphene.Mutation):
    Output = ResendConfirmationResponse

    class Arguments:
        username = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = resend_confirmation(kwargs["username"])

        if not resp["success"]:
            return ResendConfirmationResponse(
                is_successful=False, error=resp["message"]
            )

        return ResendConfirmationResponse(
            is_successful=True,
            error=None,
        )


class Mutation(graphene.ObjectType):
    resend_confirmation = ResendConfirmationMutation.Field()
