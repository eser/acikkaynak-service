from django.apps import AppConfig


class CertificatesConfig(AppConfig):
    name = "app.certificates"
    label = "certificates"
    verbose_name = "Certificates"

    def ready(self):
        # pylint:disable=import-outside-toplevel, unused-import
        import app.certificates.signals
