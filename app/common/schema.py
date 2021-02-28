import graphene

from .types import CurrencyTypes, Genders
from .schemas import languages
from .schemas import countries
from .schemas import cities
from .schemas import auth_check_user
from .schemas import auth_login
from .schemas import auth_signup
from .schemas import auth_signup_confirm
from .schemas import auth_reset_password
from .schemas import auth_reset_password_confirm
from .schemas import auth_resend_confirmation
from .schemas import auth_change_password


# enum schemas
CurrencyTypesSchema = graphene.Enum.from_enum(CurrencyTypes)
GendersSchema = graphene.Enum.from_enum(Genders)


# queries


# pylint:disable=too-many-ancestors
class Query(
    languages.Query,
    countries.Query,
    cities.Query,
    auth_check_user.Query,
    auth_login.Query,
    auth_signup.Query,
    auth_signup_confirm.Query,
    auth_reset_password.Query,
    auth_reset_password_confirm.Query,
    auth_resend_confirmation.Query,
    auth_change_password.Query,
    graphene.ObjectType,
):
    pass


# mutations


# pylint:disable=too-many-ancestors
class Mutation(
    languages.Mutation,
    countries.Mutation,
    auth_check_user.Mutation,
    auth_login.Mutation,
    auth_signup.Mutation,
    auth_signup_confirm.Mutation,
    auth_reset_password.Mutation,
    auth_reset_password_confirm.Mutation,
    auth_resend_confirmation.Mutation,
    auth_change_password.Mutation,
    graphene.ObjectType,
):
    pass
