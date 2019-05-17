from pytest import mark

from django.shortcuts import reverse
from django.test import override_settings

from tests import factories


pytestmark = mark.django_db


@override_settings(DEBUG=True, DEMO_INSPECTOR_USERNAME='inspector@test.com')
def test_demo_user_is_logged_in_when_requesting_demo_page(client):
    factories.UserFactory(username='inspector@test.com', is_superuser=False, is_staff=False)
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert session_user.is_authenticated


@override_settings(DEBUG=True, DEMO_INSPECTOR_USERNAME='inspector@test.com')
def test_demo_user_is_not_logged_in_if_superuser(client):
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = True
    user.is_staff = False
    user.save()
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated


@override_settings(DEBUG=True, DEMO_INSPECTOR_USERNAME='inspector@test.com')
def test_demo_user_is_not_logged_in_if_staff(client):
    user = factories.UserFactory(username='inspector@test.com')
    user.is_superuser = False
    user.is_staff = True
    user.save()
    response = client.get(reverse('demo-inspector'))
    assert response.status_code == 302
    response = client.get('/')
    session_user = response.context['user']
    assert not session_user.is_authenticated
