from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group as BaseGroup
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers.user_manager import UserManager
from .types import Genders


class Language(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    iso_code = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self):
        return f"{self.name} ({self.iso_code})"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class Country(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    iso_code = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class City(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    country = models.ForeignKey(
        verbose_name=_("country"),
        db_column="country_uuid",
        to=Country,
        related_name="cities",
        on_delete=models.RESTRICT,
        db_index=True,
    )
    name = models.CharField(
        max_length=255, validators=[validators.ProhibitNullCharactersValidator()]
    )

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    username = models.CharField(
        _("username"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text=_(
            "Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        # validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
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
    locale = models.CharField(
        verbose_name=_("locale"), max_length=255, default=settings.LOCALE_DEFAULT
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now
    )
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        null=True, blank=True, auto_now=True
    )  # editable=False,
    deleted_at = models.DateTimeField(editable=False, null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        # return f"{self.username} ({self.email})"
        return f"{self.pk}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class Group(BaseGroup):
    class Meta:
        app_label = "common"
