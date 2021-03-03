from django.contrib import admin
from django.utils.html import format_html
from .models import Certificate, CertificateClaim, CertificateRequirement, CertificateCategory


class CertificateRequirementInline(admin.TabularInline):
    model = CertificateRequirement
    extra = 0


class CertificateClaimAdmin(admin.ModelAdmin):
    search_fields = ("profile__slug", "profile__first_name", "profile__last_name", "certificate__slug", "certificate__name")

    list_display = ("profile", "certificate", "type")
    

class CertificateCategoryAdmin(admin.ModelAdmin):
    search_fields = ("slug", "name")

    list_display = ("name",)


class CertificateAdmin(admin.ModelAdmin):
    search_fields = ("slug", "name")
    date_hierarchy = "created_at"

    list_display = ("validated_title", "name", "status", "type", "created_at", "updated_at")
    list_filter = ("status", "type")

    inlines = (
        CertificateRequirementInline,
    )

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

admin.site.register(Certificate, CertificateAdmin)
admin.site.register(CertificateClaim, CertificateClaimAdmin)
admin.site.register(CertificateCategory, CertificateCategoryAdmin)
