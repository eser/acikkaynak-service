from uuid import uuid4
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from app.profiles.models import Profile
from .types import CertificateTypes, CertificateStatuses, CertificateClaimStatuses


class CertificateCategory(models.Model):
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
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )
    description = models.TextField(
        verbose_name=_("description"),
        # null=True,
        blank=True,
        validators=[validators.ProhibitNullCharactersValidator()],
    )

    class Meta:
        verbose_name = _("certificate category")
        verbose_name_plural = _("certificate categories")

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Certificate(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    certificate_category = models.ForeignKey(
        verbose_name=_("certificate category"),
        db_column="certificate_category_uuid",
        to=CertificateCategory,
        related_name="certificates",
        on_delete=models.RESTRICT,
        db_index=True,
    )
    certificate_category_weight = models.IntegerField(
        verbose_name=_("certificate category weight")
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
    description = models.TextField(
        verbose_name=_("description"),
        # null=True,
        blank=True,
        validators=[validators.ProhibitNullCharactersValidator()],
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


class CertificateRequirement(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    certificate = models.ForeignKey(
        verbose_name=_("certificate"),
        db_column="certificate_uuid",
        to=Certificate,
        related_name="requirements",
        on_delete=models.CASCADE,
        db_index=True,
    )
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )
    description = models.TextField(
        verbose_name=_("description"),
        # null=True,
        blank=True,
        validators=[validators.ProhibitNullCharactersValidator()],
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
        verbose_name = _("certificate requirement")
        verbose_name_plural = _("certificate requirements")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class CertificateClaim(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    certificate = models.ForeignKey(
        verbose_name=_("certificate"),
        db_column="certificate_uuid",
        to=Certificate,
        related_name="claims",
        on_delete=models.CASCADE,
        db_index=True,
    )
    profile = models.ForeignKey(
        verbose_name=_("profile"),
        db_column="profile_uuid",
        to=Profile,
        related_name="certificate_claims",
        on_delete=models.CASCADE,
        db_index=True,
    )
    type = models.CharField(
        verbose_name=_("type"),
        max_length=255,
        choices=CertificateClaimStatuses.choices(),
        default=CertificateClaimStatuses.AWAITING_APPROVAL,
    )
    applied_at = models.DateTimeField(
        verbose_name=_("applied at")
    )
    response_issued_at = models.DateTimeField(
        verbose_name=_("response issued at"), null=True, blank=False
    )
    response_comments = models.TextField(
        verbose_name=_("response comments"),
        # null=True,
        blank=True,
        validators=[validators.ProhibitNullCharactersValidator()],
    )
    expires_at = models.DateTimeField(
        verbose_name=_("expires at"), null=True, blank=True
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
        verbose_name = _("certificate claim")
        verbose_name_plural = _("certificate claims")

    def __str__(self):
        return f"{self.pk}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
