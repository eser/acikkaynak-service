from uuid import uuid4
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from .types import CertificateTypes, CertificateStatuses


class Certificate(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=255,
        unique=True,
        db_index=True,
        validators=[validators.validate_slug],
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=255,
        choices=CertificateStatuses.choices(),
        default=CertificateStatuses.ACTIVE,
    )
    type = models.CharField(
        verbose_name=_("type"),
        max_length=255,
        choices=CertificateTypes.choices(),
        default=CertificateTypes.PROGRAM,
    )
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"), editable=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), null=True, blank=True, auto_now=True
    )  # editable=False,
    deleted_at = models.DateTimeField(
        verbose_name=_("deleted at"), editable=False, null=True, blank=True
    )

    class Meta:
        verbose_name = _("certificate")
        verbose_name_plural = _("certificates")

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
