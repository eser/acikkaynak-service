from django.contrib import admin
from .models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    # search_fields = ("uuid",)
    # date_hierarchy = "created_at"

    list_display = ("uuid", "created_at", "updated_at")
    # list_filter = ("status", "type")


admin.site.register(Achievement, AchievementAdmin)
