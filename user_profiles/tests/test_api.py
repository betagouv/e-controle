from pytest import mark

from django.shortcuts import reverse

from rest_framework.test import APIClient

from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()


def test_list_users():
    inspector = factories.UserProfileFactory()
    audited = factories.UserProfileFactory()
    utils.login(client, user=inspector.user)
    url = reverse('api:user-list')
    response = client.get(url)
    assert response.status_code == 200
