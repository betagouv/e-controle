from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = 'control'
    verbose_name = "Control"

    def ready(self):
        import control.signals  # noqa
