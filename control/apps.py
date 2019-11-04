import sys

from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = 'control'
    verbose_name = "Control"

    def ready(self):
        if 'migrate' not in sys.argv:
            import control.signals  # noqa
