from django.dispatch import receiver

from .api_views import soft_delete
from control.models import Control


#@receiver(soft_delete, sender=Control)
def send_email_after_control_soft_delete(sender, obj, *args, **kwargs):
    """
    After a control is soft-deleted, we send an email to the inspector team.
    """
    import ipdb
    ipdb.set_trace()

soft_delete.connect(send_email_after_control_soft_delete, sender=Control)
