from django.apps import AppConfig


class GuideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.guide"
    verbose_name = "Гайд-карточки"

    def ready(self):
        from . import signals
