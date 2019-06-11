from pytest import mark

from django.shortcuts import reverse

from tests import factories


pytestmark = mark.django_db


def test_demo_user_is_logged_in_when_requesting_demo_page(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    factories.UserFactory(username='inspector@test.com', is_superuser=False, is_staff=False)
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert session_user.is_authenticated


def test_login_as_demo_user_is_not_available_if_debug_mode_if_off(client, settings):
    settings.DEBUG = False
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    factories.UserFactory(username='inspector@test.com', is_superuser=False, is_staff=False)
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 404
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated


def test_login_as_demo_user_is_not_available_if_setting_prevents(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = False
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    factories.UserFactory(username='inspector@test.com', is_superuser=False, is_staff=False)
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 404
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated


def test_demo_user_is_not_logged_in_if_superuser(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = True
    user.is_staff = False
    user.save()
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated


def test_demo_user_is_not_logged_in_if_staff(client, settings):
    settings.DEBUG = True
    settings.ALLOW_DEMO_LOGIN = True
    settings.DEMO_INSPECTOR_USERNAME = 'inspector@test.com'
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = False
    user.is_staff = True
    user.save()
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated
