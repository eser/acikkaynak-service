from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = "app.profiles"
    label = "profiles"
    verbose_name = "Profiles"

    def ready(self):
        # pylint:disable=import-outside-toplevel, unused-import
        import app.profiles.signals
