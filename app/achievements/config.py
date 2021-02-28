from django.apps import AppConfig


class AchievementsConfig(AppConfig):
    name = "app.achievements"
    label = "achievements"
    verbose_name = "Achievements"

    def ready(self):
        # pylint:disable=import-outside-toplevel, unused-import
        import app.achievements.signals
