from django.apps import AppConfig


class SplitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "split"

    def ready(self):
        import split.signals
        return super().ready()
