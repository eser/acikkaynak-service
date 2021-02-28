import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.schemas.languages import LanguageNode
from app.profiles.models import Profile, ProfileTag


# queries


class ProfileTagNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)

    class Meta:
        model = ProfileTag
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "slug": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
        }


class ProfileNode(DjangoObjectType):
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


class Query(graphene.ObjectType):
    profile = graphene.relay.Node.Field(ProfileNode)
    profile_by_uuid = graphene.Field(ProfileNode, uuid=graphene.UUID(required=True))
    profile_by_slug = graphene.Field(ProfileNode, slug=graphene.String(required=True))
    profiles_all = DjangoFilterConnectionField(ProfileNode)
    profile_tag = graphene.relay.Node.Field(ProfileTagNode)
    profile_tag_by_uuid = graphene.Field(ProfileTagNode, uuid=graphene.UUID(required=True))
    profile_tag_by_slug = graphene.Field(ProfileTagNode, slug=graphene.String(required=True))
    profile_tags_all = DjangoFilterConnectionField(ProfileTagNode)

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

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_profile_tag_by_uuid(parent, info, uuid):
        try:
            return ProfileTag.objects.get(uuid=uuid)
        except ProfileTag.DoesNotExist:
            return None

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_profile_tag_by_slug(parent, info, slug):
        try:
            return ProfileTag.objects.get(slug=slug)
        except ProfileTag.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
