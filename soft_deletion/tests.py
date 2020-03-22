from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient

from control.models import Control
from tests import factories, utils
from user_profiles.models import UserProfile


pytestmark = mark.django_db
client = APIClient()


User = get_user_model()


def test_inspector_can_delete_a_control():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    control = factories.ControlFactory()
    inspector.controls.add(control)
    utils.login(client, user=inspector.user)
    url = reverse('api:deletion-delete-control', args=[control.pk])
    count_before = Control.objects.active().count()
    response = client.post(url)
    count_after = Control.objects.active().count()
    assert count_after == count_before - 1
    assert response.status_code == 200
