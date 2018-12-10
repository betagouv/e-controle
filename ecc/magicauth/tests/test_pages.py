from pytest import mark

from django.core import mail
from django.shortcuts import reverse

from magicauth.models import MagicToken

from tests import factories

pytestmark = mark.django_db


def test_posting_email_for_valid_existing_user_redirects(client):
    user = factories.UserFactory()
    url = reverse('magicauth-login')
    data = {'email': user.email}
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert len(mail.outbox) == 1


def test_posting_unknown_email_raise_error(client):
    url = reverse('magicauth-login')
    data = {'email': 'unknown@email.com'}
    response = client.post(url, data=data)
    assert 'invalid' in str(response.content)
    assert len(mail.outbox) == 0


def test_posting_email_for_valid_existing_user_sends_email(client):
    user = factories.UserFactory()
    url = reverse('magicauth-login')
    data = {'email': user.email}
    client.post(url, data=data)
    assert len(mail.outbox) == 1


def test_posting_unknown_email_does_not_send_email(client):
    url = reverse('magicauth-login')
    data = {'email': 'unknown@email.com'}
    client.post(url, data=data)
    assert len(mail.outbox) == 0


def test_posting_email_for_valid_existing_user_created_token(client):
    user = factories.UserFactory()
    url = reverse('magicauth-login')
    data = {'email': user.email}
    count_before = MagicToken.objects.count()
    client.post(url, data=data)
    count_after = MagicToken.objects.count()
    assert count_after == count_before + 1
