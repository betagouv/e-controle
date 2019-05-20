from pytest import mark

from django.contrib.auth import get_user_model


from tests import factories


pytestmark = mark.django_db
User = get_user_model()


def test_username_is_saved_as_lowercase(client):
    assert not User.objects.filter(username='someone@test.com').exists()
    factories.UserFactory(username='SOMEONE@test.com')
    assert User.objects.filter(username='someone@test.com').exists()


def test_email_is_saved_as_lowercase(client):
    assert not User.objects.filter(email='someone@test.com').exists()
    factories.UserFactory(email='SOMEONE@test.com')
    assert User.objects.filter(email='someone@test.com').exists()
