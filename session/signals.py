from django.contrib.auth import get_user_model
from user_profiles.models import UserIpAddress
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from actstream import action

User = get_user_model()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def save_ip_address(request):
    userIp = UserIpAddress(ip=get_client_ip(request), username=request.user)
    userIp.save()

@receiver(user_logged_in, sender=User)
def add_action_log_for_login(sender, user, request, **kwargs):
    save_ip_address(request)

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
