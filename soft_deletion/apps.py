import sys

from django.apps import AppConfig


class SoftDeletionConfig(AppConfig):
    name = 'soft_deletion'
    verbose_name = "Suppression"

    def ready(self):
        if 'migrate' not in sys.argv:
            import soft_deletion.signals  # noqa
