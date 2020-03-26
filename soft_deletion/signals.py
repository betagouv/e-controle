from django.dispatch import receiver
from utils.email import send_email

from control.models import Control
from .api_views import soft_delete_signal
from user_profiles.models import UserProfile


@receiver(soft_delete_signal, sender=Control)
def send_email_after_control_soft_delete(session_user, obj, *args, **kwargs):
    """
    After a control is soft-deleted, we send an email to the inspector team.
    """
    control = obj
    inspectors = control.user_profiles.filter(profile_type=UserProfile.INSPECTOR)
    inspectors_emails = inspectors.values_list('user__email', flat=True)
    context = {
        'deleter_user': session_user,
        'control': control,
        'inspectors': inspectors
    }
    subject = f'e.contrôle - Suppression de l\'espace - {control}'

    send_email(
        to=inspectors_emails,
        subject=subject,
        html_template='soft_deletion/email_delete_control.html',
        text_template='soft_deletion/email_delete_control.txt',
        extra_context=context,
    )
