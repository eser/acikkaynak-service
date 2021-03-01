import graphene
from django.conf import settings
from graphene_django.debug import DjangoDebug
import app.common.schema
import app.profiles.schema
import app.certificates.schema


# queries


# pylint:disable=too-many-ancestors
class Query(
    app.common.schema.Query,
    app.profiles.schema.Query,
    app.certificates.schema.Query,
    graphene.ObjectType,
):
    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name="_debug")


# mutations


# pylint:disable=too-many-ancestors
class Mutation(
    app.common.schema.Mutation,
    app.profiles.schema.Mutation,
    app.certificates.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
