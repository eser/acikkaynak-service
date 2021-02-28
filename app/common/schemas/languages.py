import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.models import Language


# queries


class LanguageNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Language
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "iso_code": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
        }


class Query(graphene.ObjectType):
    language = graphene.relay.Node.Field(LanguageNode)
    language_by_iso_code = graphene.Field(
        LanguageNode, iso_code=graphene.String(required=True)
    )
    languages_all = DjangoFilterConnectionField(LanguageNode)

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_language_by_iso_code(parent, info, iso_code):
        try:
            return Language.objects.get(iso_code=iso_code)
        except Language.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
