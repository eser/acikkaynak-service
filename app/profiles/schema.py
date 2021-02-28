import graphene
from .schemas import queries
from .schemas import update


# queries


# pylint:disable=too-many-ancestors
class Query(
    queries.Query,
    update.Query,
    graphene.ObjectType,
):
    pass


# mutations


# pylint:disable=too-many-ancestors
class Mutation(
    queries.Mutation,
    update.Mutation,
    graphene.ObjectType,
):
    pass
