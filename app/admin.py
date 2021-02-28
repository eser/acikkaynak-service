from django.contrib import admin


class AdminSite(admin.AdminSite):
    site_title = "açık-kaynak.org admin"
    site_header = "👋🏻 açık-kaynak.org administration"
    index_title = "Sections"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        ordering = {
            "Common": 1,
            "Profiles": 2,
        }

        sorted_app_list = sorted(
            app_list,
            key=lambda x: ordering[x["name"]] if x["name"] in ordering else len(ordering) + 1
        )

        return sorted_app_list
