import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.schemas.languages import LanguageNode
from app.profiles.models import Profile


# queries


class ProfileNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)
    languages = graphene.List(LanguageNode)

    class Meta:
        model = Profile
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
            "phone": ["exact", "icontains", "istartswith"],
        }

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_languages(parent, info):
        return parent.languages.all()


class Query(graphene.ObjectType):
    profile = graphene.relay.Node.Field(ProfileNode)
    profile_by_uuid = graphene.Field(ProfileNode, uuid=graphene.UUID(required=True))
    profile_by_slug = graphene.Field(ProfileNode, slug=graphene.String(required=True))
    profiles_all = DjangoFilterConnectionField(ProfileNode)

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_profile_by_uuid(parent, info, uuid):
        try:
            return Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_profile_by_slug(parent, info, slug):
        try:
            return Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
