from pytest import mark

from django.test import override_settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


pytestmark = mark.django_db

User = get_user_model()


ADMIN_USER_DATA = {
  'username': 'test@test.com',
  'email': 'test@test.com',
  'password': 'test12345',
}


def test_super_user_can_login_to_admin(client):
    User.objects.create_superuser(**ADMIN_USER_DATA)
    assert '_auth_user_id' not in client.session
    url = reverse('admin-login')
    client.post(url, ADMIN_USER_DATA)
    assert '_auth_user_id' in client.session


def test_login_to_admin_fails_if_wrong_credentials(client):
    User.objects.create_superuser(**ADMIN_USER_DATA)
    wrong_data = ADMIN_USER_DATA.copy()
    wrong_data['password'] = 'wrong_password'
    assert '_auth_user_id' not in client.session
    url = reverse('admin-login')
    client.post(url, wrong_data)
    assert '_auth_user_id' not in client.session


@override_settings(ADMIN_URL='admin/')
def test_login_to_admin_redirects(client):
    User.objects.create_superuser(**ADMIN_USER_DATA)
    url = reverse('admin-login')
    response = client.post(url, ADMIN_USER_DATA)
    assert response.status_code == 302
    assert 'admin/' in response.url


@override_settings(ADMIN_URL='admin/')
def test_login_to_admin_does_not_redirect_to_next(client):
    User.objects.create_superuser(**ADMIN_USER_DATA)
    url = reverse('admin-login')
    url += '?next=/unwanted/'
    response = client.post(url, ADMIN_USER_DATA)
    assert response.status_code == 302
    assert '/unwanted/' not in response.url
    assert 'admin/' in response.url
