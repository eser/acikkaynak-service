from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from app.profiles.models import Profile
from .types import AchievementTypes

class Achievement(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    type = models.CharField(
        verbose_name=_("type"), null=False, blank=False, max_length=255,
        choices=AchievementTypes.choices(),
        default=AchievementTypes.CLASS_ATTEND,
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
        verbose_name = _("achievement")
        verbose_name_plural = _("achievements")

    def __str__(self):
        return f"{self.pk}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
