from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient

from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()

User = get_user_model()


def test_logged_in_user_can_list_users():
    factories.UserProfileFactory()
    user = factories.UserFactory()
    utils.login(client, user=user)
    url = reverse('api:user-list')
    response = client.get(url)
    assert response.status_code == 200


def test_inspector_can_create_user():
    inspector = factories.UserProfileFactory(profile_type='inspector')
    control = factories.ControlFactory()
    inspector.controls.add(control)
    post_data = {
        'first_name': 'Marcel',
        'last_name': 'Proust',
        'profile_type': 'audited',
        'email': 'marcel@proust.com',
        'controls': [control.id]
    }
    utils.login(client, user=inspector.user)
    url = reverse('api:user-list')
    count_before = User.objects.count()
    response = client.post(url, post_data)
    count_after = User.objects.count()
    assert count_after == count_before + 1
    assert response.status_code == 201


def test_audited_cannot_create_user():
    audited = factories.UserProfileFactory(profile_type='audited')
    control = factories.ControlFactory()
    audited.controls.add(control)
    post_data = {
        'first_name': 'Inspector',
        'last_name': 'Gadget',
        'profile_type': 'inspector',
        'email': 'inspector@gadget.com',
        'controls': [control.id]
    }
    utils.login(client, user=audited.user)
    url = reverse('api:user-list')
    count_before = User.objects.count()
    response = client.post(url, post_data)
    count_after = User.objects.count()
    assert count_after == count_before
    assert response.status_code != 201


def test_inspector_can_deactivate_user():
    someone = factories.UserProfileFactory(profile_type='audited')
    inspector = factories.UserProfileFactory(profile_type='inspector')
    control = factories.ControlFactory()
    inspector.controls.add(control)
    someone.controls.add(control)
    utils.login(client, user=inspector.user)
    url = reverse('api:user-deactivate', args=[someone.pk])
    count_before = User.objects.filter(is_active=True).count()
    response = client.post(url)
    count_after = User.objects.filter(is_active=True).count()
    assert count_after == count_before - 1
    assert response.status_code == 200


def test_audited_cannot_deactivate_user():
    someone = factories.UserProfileFactory(profile_type='inspector')
    audited = factories.UserProfileFactory(profile_type='audited')
    control = factories.ControlFactory()
    audited.controls.add(control)
    someone.controls.add(control)
    utils.login(client, user=audited.user)
    url = reverse('api:user-deactivate', args=[someone.pk])
    count_before = User.objects.filter(is_active=True).count()
    response = client.post(url)
    count_after = User.objects.filter(is_active=True).count()
    assert count_after == count_before
    assert response.status_code != 200
