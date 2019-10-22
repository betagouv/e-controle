from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from actstream import action

from .api_views import user_api_post_remove
from .models import UserProfile
from .serializers import user_api_post_add, user_api_post_update
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


def bake_and_send_email(
        session_user, user_profile, control, email_subject, html_template, text_template):
    """
    A wrapper function for sending emails.
    """
    recipients = [session_user.email, ]
    inspectors = control.user_profiles.filter(profile_type=UserProfile.INSPECTOR)
    inspectors = inspectors.exclude(user=session_user)
    inspectors_emails = inspectors.values_list('user__email', flat=True)
    context = {
        'control': control,
        'user': session_user,
        'target_user': user_profile.user
    }
    send_email(
        to=recipients,
        cc=inspectors_emails,
        subject=email_subject,
        html_template=html_template,
        text_template=text_template,
        extra_context=context,
    )


def send_email_for_user_add(session_user, user_profile, control, **kwargs):
    """
    Send an email to notify that a user has been added.
    """
    bake_and_send_email(
        session_user=session_user,
        user_profile=user_profile,
        control=control,
        email_subject=f'e.contrôle - Nouvel utilisateur - {control}',
        html_template='user_profiles/email_add_user.html',
        text_template='user_profiles/email_add_user.txt',
    )


def send_email_for_user_remove(session_user, user_profile, control, **kwargs):
    """
    Send an email to notify that a user has been removed.
    """
    bake_and_send_email(
        session_user=session_user,
        user_profile=user_profile,
        control=control,
        email_subject=f'e.contrôle - Suppression utilisateur - {control}',
        html_template='user_profiles/email_remove_user.html',
        text_template='user_profiles/email_remove_user.txt',
    )


if settings.SEND_EMAIL_WHEN_USER_ADDED:
    user_api_post_add.connect(send_email_for_user_add, sender=UserProfile)

if settings.SEND_EMAIL_WHEN_USER_REMOVED:
    user_api_post_remove.connect(send_email_for_user_remove, sender=UserProfile)
