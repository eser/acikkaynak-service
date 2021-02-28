from django.conf import settings
import graphene
from app.common.auth.signup import signup
from app.common.models import Genders

# queries


class Query(graphene.ObjectType):
    pass


# mutations


class SignupResponseConfirmationCodeDetails(graphene.ObjectType):
    attribute_name = graphene.String()
    delivery_medium = graphene.String()
    destination = graphene.String()


class SignupResponse(graphene.ObjectType):
    is_successful = graphene.Boolean()
    error = graphene.String()
    confirmation_code = graphene.Field(SignupResponseConfirmationCodeDetails)
    # user_confirmed = graphene.Boolean()
    username = graphene.String()


class SignupMutation(graphene.Mutation):
    Output = SignupResponse

    class Arguments:
        login = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String()
        birthdate = graphene.Date()
        email = graphene.String()
        phone = graphene.String()
        profile_picture_uri = graphene.String()
        locale = graphene.String()

    # pylint:disable=unused-argument
    @classmethod
    def mutate(cls, root, info, **kwargs):
        resp = signup(
            kwargs["login"],
            kwargs["password"],
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            gender=kwargs.get("gender", Genders.OTHER),
            birthdate=kwargs.get("birthdate"),
            email=kwargs.get("email"),
            phone=kwargs.get("phone"),
            profile_picture_uri=kwargs.get("profile_picture_uri"),
            locale=kwargs.get("locale", settings.LOCALE_DEFAULT),
        )

        if not resp["success"]:
            return SignupResponse(
                is_successful=False,
                error=resp["message"],
                confirmation_code=None,
                username=None,
            )  # user_confirmed=None,

        return SignupResponse(
            is_successful=True,
            error=None,
            confirmation_code=SignupResponseConfirmationCodeDetails(
                attribute_name=resp["data"]["code_delivery_details"]["attribute_name"],
                delivery_medium=resp["data"]["code_delivery_details"][
                    "delivery_medium"
                ],
                destination=resp["data"]["code_delivery_details"]["destination"],
            ),
            # user_confirmed = resp["data"]["user_confirmed"],
            username=resp["data"]["user_sub"],
        )


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()
