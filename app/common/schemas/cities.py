import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.models import City


# queries


class CityNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)

    class Meta:
        model = City
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "country": ["exact"],
        }


class Query(graphene.ObjectType):
    city = graphene.relay.Node.Field(CityNode)
    cities_all = DjangoFilterConnectionField(CityNode)


# mutations


class Mutation(graphene.ObjectType):
    pass
