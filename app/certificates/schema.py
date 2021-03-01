import graphene
from .schemas import queries


# queries


# pylint:disable=too-many-ancestors
class Query(
    queries.Query,
    graphene.ObjectType,
):
    pass


# mutations


# pylint:disable=too-many-ancestors
class Mutation(
    queries.Mutation,
    graphene.ObjectType,
):
    pass
