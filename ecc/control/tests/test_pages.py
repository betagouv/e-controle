from pytest import mark

from django.shortcuts import reverse

from tests import factories


pytestmark = mark.django_db


def test_send_file_wiew_works(client):
    response_file = factories.ResponseFileFactory()
    url = reverse('send-response-file', args=[response_file.id])
    response = client.get(url)
    assert response.status_code == 200
