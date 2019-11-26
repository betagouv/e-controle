from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry

from .actions import add_log_entry


@receiver(post_save, sender=LogEntry)
def log_admin_action(sender, instance, **kwargs):
    """
    Add a log entry after for admin actions
    """
    if instance.is_change():
        verb = 'admin updated'
    if instance.is_deletion():
        verb = 'admin deleted'
    if instance.is_addition():
        verb = 'admin added'
    edited_object = instance.get_edited_object()
    add_log_entry(verb, instance.user, edited_object, instance.change_message)
