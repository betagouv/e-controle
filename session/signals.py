from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from actstream import action

User = get_user_model()


@receiver(user_logged_in, sender=User)
def add_action_log_for_login(sender, user, request, **kwargs):
    action_details = {
        'sender': user,
        'verb': 'logged in',
    }
    action.send(**action_details)


@receiver(user_logged_out, sender=User)
def add_action_log_for_logout(sender, user, request, **kwargs):
    action_details = {
        'sender': user,
        'verb': 'logged out',
    }
    action.send(**action_details)
