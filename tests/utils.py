import importlib
import sys

from django.conf import settings
from django.urls import clear_url_caches

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
