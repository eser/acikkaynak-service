from django.contrib import admin
from .models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    search_fields = ("profile__first_name", "profile__last_name")
    date_hierarchy = "earned_at"

    list_display = ("uuid", "type", "profile", "earned_at", "created_at", "updated_at")
    list_filter = ("type", "profile")


admin.site.register(Achievement, AchievementAdmin)
