from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver


User = get_user_model()


@receiver(pre_save, sender=User)
def lowercase_username(sender, instance, *args, **kwargs):
    """
    When saving a user, we want to lowercase his username and email.
    """
    instance.username = instance.username.lower()
    instance.email = instance.email.lower()
