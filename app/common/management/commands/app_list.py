from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for app_name in settings.INSTALLED_APPS:
            if app_name.startswith("app."):
                print(app_name[4:])
