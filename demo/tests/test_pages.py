import pytest

from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch

from tests import factories, utils


pytestmark = pytest.mark.django_db


def test_demo_user_is_logged_in_when_requesting_demo_page(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    utils.reload_urlconf()
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = False
    user.is_staff = False
    user.save()
    response = client.get(reverse('demo-inspector'), follow=True)
    assert response.status_code == 200
    session_user = response.context['user']
    assert session_user.is_authenticated


def test_login_as_demo_user_is_not_available_if_debug_mode_if_off(client, settings):
    settings.DEBUG = False
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    utils.reload_urlconf()
    with pytest.raises(NoReverseMatch):
        reverse('demo-inspector')


def test_login_as_demo_user_is_not_available_if_setting_prevents(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = False
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    utils.reload_urlconf()
    with pytest.raises(NoReverseMatch):
        reverse('demo-inspector')


def test_demo_user_is_not_logged_in_if_superuser(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    utils.reload_urlconf()
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = True
    user.is_staff = False
    user.save()
    response = client.get(reverse('demo-inspector'), follow=True)
    assert response.status_code != 200


def test_demo_user_is_not_logged_in_if_staff(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    utils.reload_urlconf()
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = False
    user.is_staff = True
    user.save()
    response = client.get(reverse('demo-inspector'), follow=True)
    assert response.status_code != 200


def test_demo_user_is_not_logged_in_if_username_not_in_setting(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = None
    utils.reload_urlconf()
    response = client.get(reverse('demo-inspector'), follow=True)
    assert response.status_code != 200
