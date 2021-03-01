import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.schemas.languages import LanguageNode
from app.certificates.models import Certificate


# queries


class CertificateNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Certificate
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
        }


class Query(graphene.ObjectType):
    certificate = graphene.relay.Node.Field(CertificateNode)
    certificate_by_uuid = graphene.Field(CertificateNode, uuid=graphene.UUID(required=True))
    certificates_all = DjangoFilterConnectionField(CertificateNode)

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_certificate_by_uuid(parent, info, uuid):
        try:
            return Certificate.objects.get(uuid=uuid)
        except Certificate.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
