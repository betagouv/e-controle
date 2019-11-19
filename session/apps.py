import sys

from django.apps import AppConfig


class SessionConfig(AppConfig):
    name = 'session'
    verbose_name = "session"

    def ready(self):
        if 'migrate' not in sys.argv:
            import session.signals  # noqa
