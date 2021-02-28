from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("slug", "first_name", "last_name", "email", "phone")
    date_hierarchy = "created_at"

    list_display = ("validated_title", "first_name", "last_name", "status", "type", "email", "phone", "created_at", "updated_at")
    list_filter = ("status", "type")

    @staticmethod
    def validated_title(row):
        if row.deleted_at is not None:
            return format_html(
                "<del>{}</del>",
                row.slug,
            )

        return format_html(
            "{}",
            row.slug,
        )

    validated_title.short_description = "Slug"
    validated_title.admin_order_field = "slug"


admin.site.register(Profile, ProfileAdmin)
