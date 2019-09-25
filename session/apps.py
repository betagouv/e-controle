from django.apps import AppConfig


class SessionConfig(AppConfig):
    name = 'session'
    verbose_name = "session"

    def ready(self):
        import session.signals  # noqa
