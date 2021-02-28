import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.models import Country


# queries


class CountryNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Country
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "iso_code": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
        }


class Query(graphene.ObjectType):
    country = graphene.relay.Node.Field(CountryNode)
    country_by_iso_code = graphene.Field(
        CountryNode, iso_code=graphene.String(required=True)
    )
    countries_all = DjangoFilterConnectionField(CountryNode)

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_country_by_iso_code(parent, info, iso_code):
        try:
            return Country.objects.get(iso_code=iso_code)
        except Country.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
