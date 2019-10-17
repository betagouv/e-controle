from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.core import mail

from rest_framework.test import APIClient

from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()

User = get_user_model()


def test_an_email_is_sent_when_user_is_created():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    control = factories.ControlFactory()
    inspector.controls.add(control)
    post_data = {
        'first_name': 'Marcel',
        'last_name': 'Proust',
        'profile_type': UserProfile.AUDITED,
        'email': 'marcel@proust.com',
        'control': control.id,
    }
    utils.login(client, user=inspector.user)
    url = reverse('api:user-list')
    count_emails_before = len(mail.outbox)
    count_users_before = User.objects.count()
    client.post(url, post_data)
    count_emails_after = len(mail.outbox)
    count_users_after = User.objects.count()
    assert count_users_after == count_users_before + 1
    assert count_emails_after == count_emails_before + 1
