from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group as OldGroup
from .models import Language, Country, City, User, Group


class LanguageAdmin(admin.ModelAdmin):
    list_display = ("iso_code", "name")
    list_filter = ()


class CountryAdmin(admin.ModelAdmin):
    list_display = ("iso_code", "name")
    list_filter = ()


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_joined",
    )
    list_filter = ()


admin.site.unregister(OldGroup)

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
