from uuid import uuid4
from django.conf import settings
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from app.common.models import Language, Country, City
from app.common.types import Genders
from .types import ProfileStatuses, ProfileTypes, ProfileAchievementTypes


class ProfileTag(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
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

    class Meta:
        verbose_name = _("profile tag")
        verbose_name_plural = _("profile tags")

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class Profile(models.Model):
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
    users = models.ManyToManyField(
        verbose_name=_("users"), to=settings.AUTH_USER_MODEL, related_name="profiles"
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=255,
        choices=ProfileStatuses.choices(),
        default=ProfileStatuses.ACTIVE,
    )
    type = models.CharField(
        verbose_name=_("type"),
        max_length=255,
        choices=ProfileTypes.choices(),
        default=ProfileTypes.INDIVIDUAL,
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=255,
        validators=[
            validators.ProhibitNullCharactersValidator(),
            validators.MinLengthValidator(2),
        ],
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=255,
        validators=[
            validators.ProhibitNullCharactersValidator(),
            validators.MinLengthValidator(2),
        ],
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=255,
        choices=Genders.choices(),
        default=Genders.OTHER,
    )
    birthdate = models.DateField(verbose_name=_("birthdate"), null=True, blank=True)
    email = models.EmailField(
        verbose_name=_("e-mail"),
        max_length=255,
        unique=True,
        validators=[
            validators.ProhibitNullCharactersValidator(),
            validators.EmailValidator(),
        ],
    )
    phone = models.CharField(
        verbose_name=_("phone"), max_length=255, null=True, blank=True
    )
    profile_picture_uri = models.URLField(
        verbose_name=_("profile picture uri"),
        null=True,
        blank=True,
        validators=[validators.URLValidator()],
    )
    bio = models.TextField(
        verbose_name=_("bio"),
        # null=True,
        blank=True,
        default="",
        validators=[validators.ProhibitNullCharactersValidator()],
    )
    location_city = models.ForeignKey(
        verbose_name=_("location city"),
        db_column="location_city_uuid",
        to=City,
        null=True,
        blank=True,
        default=None,
        on_delete=models.RESTRICT,
        db_index=True,
    )
    location_country = models.ForeignKey(
        verbose_name=_("location country"),
        db_column="location_country_uuid",
        to=Country,
        null=True,
        blank=True,
        default=None,
        on_delete=models.RESTRICT,
        db_index=True,
    )
    tags = models.ManyToManyField(
        verbose_name=_("tags"), to=ProfileTag, related_name="tags"
    )
    languages = models.ManyToManyField(
        verbose_name=_("languages"), to=Language, related_name="profiles"
    )  # , on_delete=models.RESTRICT
    timezone = models.CharField(
        verbose_name=_("timezone"),
        max_length=255,
        default="Europe/Berlin",
    )
    notification_messages = models.BooleanField(
        _("notification messages"),
        default=True,
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
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class ProfileAchievement(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    type = models.CharField(
        verbose_name=_("type"), null=False, blank=False, max_length=255,
        choices=ProfileAchievementTypes.choices(),
        default=ProfileAchievementTypes.CLASS_ATTEND,
    )
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="achievements")
    earned_at = models.DateTimeField(
        verbose_name=_("earned at"),
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
        verbose_name = _("profile achievement")
        verbose_name_plural = _("profile achievements")

    def __str__(self):
        return f"{self.pk}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
