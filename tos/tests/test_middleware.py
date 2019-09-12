from pytest import mark
from rest_framework.test import APIClient

from django.shortcuts import reverse
from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


def make_user(agreed_to_tos):
    user_profile = factories.UserProfileFactory(agreed_to_tos=agreed_to_tos)
    return user_profile.user


def test_user_who_did_not_agree_to_tos_is_redirected():
    user = make_user(agreed_to_tos=False)
    utils.login(client, user=user)
    url = reverse('questionnaire-list')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('welcome')


def test_user_who_agreed_to_tos_is_not_redirected():
    user = make_user(agreed_to_tos=True)

    utils.login(client, user=user)
    url = reverse('questionnaire-list')

    response = client.get(url)

    assert response.status_code == 200


def test_anonymous_user_is_not_redirected():
    url = reverse('questionnaire-list')

    response = client.get(url)

    # redirected to login, not welcome
    assert response.status_code == 302
    assert response.url != reverse('welcome')


def test_do_not_redirect_logout():
    user = make_user(agreed_to_tos=False)
    utils.login(client, user=user)
    url = reverse('logout')

    response = client.get(url)

    # redirected but not to welcome
    assert response.status_code == 302
    assert response.url != reverse('welcome')
