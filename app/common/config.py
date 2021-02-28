from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "app.common"
    label = "common"
    verbose_name = "Common"

    def ready(self):
        # pylint:disable=import-outside-toplevel, unused-import
        import app.common.signals
