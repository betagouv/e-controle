from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from actstream import action

from .serializers import user_api_post_add, user_api_post_update
from .models import UserProfile
from utils.email import send_email


User = get_user_model()


@receiver(pre_save, sender=User)
def lowercase_username(sender, instance, *args, **kwargs):
    """
    When saving a user, we want to lowercase his username and email.
    """
    instance.username = instance.username.lower()
    instance.email = instance.email.lower()


def add_log_entry(verb, session_user, user_profile, control=None):
    action_details = {
        'sender': session_user,
        'action_object': user_profile,
        'target': control,
    }
    if user_profile.is_inspector:
        action_details['verb'] = f'{verb} inspector user'
    if user_profile.is_audited:
        action_details['verb'] = f'{verb} audited user'
    action.send(**action_details)


@receiver(user_api_post_add, sender=UserProfile)
def add_log_entry_for_user_add(session_user, user_profile, control, **kwargs):
    """
    Add a log entry after user is added to a control.
    """
    add_log_entry(
        verb='added', session_user=session_user, user_profile=user_profile, control=control)


@receiver(user_api_post_update, sender=UserProfile)
def add_log_entry_for_user_update(session_user, user_profile, **kwargs):
    """
    Add a log entry after user is updated to a control.
    """
    add_log_entry(verb='updated', session_user=session_user, user_profile=user_profile)


@receiver(user_api_post_add, sender=UserProfile)
def send_email_for_user_add(session_user, user_profile, control, **kwargs):
    """
    Send an email to notify that a user has been added.
    """
    email_subject = f'e.contrôle - Nouvel utilisateur - {control}'
    inspector_team = ['todo@test.com']
    context = {
        'control': control,
        'user': session_user,
        'added_user': user_profile.user
    }
    send_email(
        to=[session_user.email, ],
        cc=inspector_team,
        subject=email_subject,
        html_template='user_profiles/email_add_user.html',
        text_template='user_profiles/email_add_user.txt',
        extra_context=context,
    )
