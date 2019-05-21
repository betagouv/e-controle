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


def test_can_associate_a_control_to_anexisting_user():
    inspector = factories.UserProfileFactory(profile_type='inspector')
    control = factories.ControlFactory()
    inspector.controls.add(control)
    existing_user = factories.UserFactory()
    post_data = {
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'profile_type': 'audited',
        'email': existing_user.email,
        'organization': '',
        'controls': [control.id]
    }
    utils.login(client, user=inspector.user)
    assert control not in existing_user.profile.controls.all()
    url = reverse('api:user-list')
    count_before = User.objects.count()
    response = client.post(url, post_data)
    count_after = User.objects.count()
    assert response.status_code == 201
    assert count_after == count_before
    assert control in existing_user.profile.controls.all()


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


def test_inspector_cannot_alter_a_control_that_is_not_accessible_to_him():
    inspector = factories.UserProfileFactory(profile_type='inspector')
    control = factories.ControlFactory()
    existing_user = factories.UserFactory()
    assert control not in inspector.controls.all()
    assert control not in existing_user.profile.controls.all()
    post_data = {
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'profile_type': 'audited',
        'email': existing_user.email,
        'organization': '',
        'controls': [control.id]
    }
    utils.login(client, user=inspector.user)
    url = reverse('api:user-list')
    count_before = User.objects.count()
    response = client.post(url, post_data)
    count_after = User.objects.count()
    assert response.status_code != 201
    assert count_after == count_before
    assert control not in existing_user.profile.controls.all()


def test_inspector_can_remove_user_from_control():
    someone = factories.UserProfileFactory(profile_type='audited')
    inspector = factories.UserProfileFactory(profile_type='inspector')
    control = factories.ControlFactory()
    inspector.controls.add(control)
    someone.controls.add(control)
    utils.login(client, user=inspector.user)
    url = reverse('api:user-remove-control', args=[someone.pk])
    count_before = User.objects.filter(profile__controls=control).count()
    response = client.post(url, {'control': control.pk})
    count_after = User.objects.filter(profile__controls=control).count()
    assert count_after == count_before - 1
    assert response.status_code == 200


def test_logged_in_user_can_get_current_user():
    factories.UserProfileFactory()
    user = factories.UserFactory()
    utils.login(client, user=user)
    url = reverse('api:user-current')
    response = client.get(url)
    assert response.status_code == 200
