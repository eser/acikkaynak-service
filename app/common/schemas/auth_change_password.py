import graphene
from app.common.auth.change_password import change_password


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class ChangePasswordResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()


class ChangePasswordMutation(graphene.Mutation):
    Output = ChangePasswordResponse

    class Arguments:
        # TODO will be taken from auth header
        access_token = graphene.String(required=True)
        previous_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = change_password(
            kwargs["access_token"], kwargs["previous_password"], kwargs["new_password"]
        )

        if not resp["success"]:
            return ChangePasswordResponse(is_successful=False, error=resp["message"])

        return ChangePasswordResponse(
            is_successful=True,
            error=None,
        )


class Mutation(graphene.ObjectType):
    change_password = ChangePasswordMutation.Field()
