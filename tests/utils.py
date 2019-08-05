import importlib
import sys

from django.conf import settings
from django.urls import clear_url_caches
from user_profiles.models import UserProfile

from . import factories


def login(client, user=None):
    """
    Log a user in for the given test session.
    """
    if not user:
        user = factories.UserFactory()
    user.set_password('123')
    user.save()
    login_success = client.login(username=user.username, password='123')
    assert login_success
    return user


def reload_urlconf():
    """
    Sometimes, you need to reload Django URLs, for instance if you change
    some settings right in your tests.
    """
    clear_url_caches()
    urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        importlib.reload(sys.modules[urlconf])


def make_audited_user(control):
    user = factories.UserFactory()
    user.profile.controls.add(control)
    user.profile.save()
    return user


def make_inspector_user(control):
    user_profile = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    user_profile.controls.add(control)
    user_profile.save()
    return user_profile.user