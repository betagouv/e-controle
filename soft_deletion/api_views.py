from django.dispatch import receiver
from django.dispatch import Signal
from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response
from utils.email import send_email

from control.models import Control
from control.permissions import OnlyInspectorCanAccess

from user_profiles.models import UserProfile

soft_delete = Signal(providing_args=['obj'])


class DeleteViewSet(viewsets.ViewSet):
    permission_classes = (OnlyInspectorCanAccess,)

    def get_controls(self):
        return self.request.user.profile.controls.active()

    @decorators.action(detail=True, methods=['post'], url_path='delete-control')
    def delete_control(self, request, pk):
        control = self.get_controls().get(pk=pk)
        control.delete()
        soft_delete.send(
            sender=Control,
            session_user=request.user,
            obj=control)

        return Response({'status': f"Deleted {control}"})


@receiver(soft_delete, sender=Control)
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
    subject = f'e.contrôle - Suppression de l\'espace - {control}',

    send_email(
        to=inspectors_emails,
        subject=subject,
        html_template='soft_deletion/email_delete_control.html',
        text_template='soft_deletion/email_delete_control.txt',
        extra_context=context,
    )
