from django.apps import AppConfig
from django.apps import apps
from django.contrib.auth import get_user_model


class EccConfig(AppConfig):
    name = 'ecc'
    verbose_name = "ecc"

    def ready(self):
        from .celery import app as celery_app
        __all__ = ('celery_app',)

        from actstream import registry
        registry.register(apps.get_model('control.ResponseFile'))
        registry.register(apps.get_model('control.Control'))
        registry.register(apps.get_model('control.Question'))
        registry.register(apps.get_model('control.Questionnaire'))
        registry.register(get_user_model())
        registry.register(apps.get_model('user_profiles.UserProfile'))
