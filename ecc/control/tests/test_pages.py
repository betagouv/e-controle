from pytest import mark

from django.shortcuts import reverse

from tests import factories


pytestmark = mark.django_db


def test_send_file_wiew_works(client):
    question = factories.QuestionFactory()
    url = reverse('send-file')
    response = client.get(url)

    assert response.status_code == 200
