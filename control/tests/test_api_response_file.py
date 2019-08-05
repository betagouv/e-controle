from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import ResponseFile
from tests import factories, utils
from user_profiles.models import UserProfile


pytestmark = mark.django_db
client = APIClient()


def get_response_file(user, id):
    utils.login(client, user=user)
    url = reverse('api:response-file-detail', args=[id])
    response = client.get(url)
    return response


def trash_response_file(user, id, payload):
    utils.login(client, user=user)
    url = reverse('response-file-trash', args=[id])
    response = client.put(url, payload)
    return response


def make_audited_user(control):
    user = factories.UserFactory()
    user.profile.controls.add(control)
    user.profile.save()
    return user


def make_inspector_user(control):
    user_profile = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    user_profile.controls.add(control)
    user_profile.save()
    return user_profile.user


########## get

def test_can_get_response_file_if_control_is_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    user = make_audited_user(response_file.question.theme.questionnaire.control)

    response = get_response_file(user, response_file.id)

    assert response.status_code == 200


def test_cannot_get_response_file_if_control_is_not_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    control = factories.ControlFactory()
    user = make_audited_user(control)

    response = get_response_file(user, response_file.id)

    assert 400 <= response.status_code <= 499


def test_cannot_get_response_file_if_user_not_logged_in():
    response_file = factories.ResponseFileFactory()
    url = reverse('api:response-file-detail', args=[response_file.id])
    response = client.get(url)
    assert response.status_code == 403


########## write methods

def run_test_response_file_api_is_readonly(user, response_file):
    payload = {"id": response_file.id}
    utils.login(client, user=user)

    # no create
    url = reverse('api:response-file-list')
    response = client.post(url, payload, format='json')
    assert response.status_code == 405  # method not allowed

    # no update
    url = reverse('api:response-file-detail', args=[payload['id']])
    response = client.put(url, payload, format='json')
    assert response.status_code == 405  # method not allowed

    # no patch
    url = reverse('api:response-file-detail', args=[payload['id']])
    response = client.patch(url, payload, format='json')
    assert response.status_code == 405  # method not allowed


def test_response_file_api_is_readonly_for_audited():
    response_file = factories.ResponseFileFactory()
    user = make_audited_user(response_file.question.theme.questionnaire.control)
    run_test_response_file_api_is_readonly(user, response_file)


def test_response_file_api_is_readonly_for_inspector():
    response_file = factories.ResponseFileFactory()
    user = make_inspector_user(response_file.question.theme.questionnaire.control)
    run_test_response_file_api_is_readonly(user, response_file)


########## trash

def test_cannot_trash_response_file_if_user_not_logged_in():
    response_file = factories.ResponseFileFactory()
    url = reverse('response-file-trash', args=[response_file.id])
    response = client.get(url)
    assert response.status_code == 403


def test_cannot_trash_response_file_if_control_is_not_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    control = factories.ControlFactory()
    user = make_audited_user(control)
    payload = { "is_deleted": "true" }

    response = trash_response_file(user, response_file.id, payload)

    assert 400 <= response.status_code <= 499


def test_can_trash_response_file_if_control_is_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    user = make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }
    count_before = ResponseFile.objects.count
    assert not ResponseFile.objects.get(id=response_file.id).is_deleted

    response = trash_response_file(user, response_file.id, payload)

    assert response.status_code == 200
    count_after = ResponseFile.objects.count
    assert count_before == count_after
    assert ResponseFile.objects.get(id=response_file.id).is_deleted


def can_trash_a_trashed_file():
    response_file = factories.ResponseFileFactory(is_deleted=True)
    user = make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }

    response = trash_response_file(user, response_file.id, payload)

    assert response.status_code == 200
    assert ResponseFile.objects.get(id=response_file.id).is_deleted
