from actstream.models import Action
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch
from pytest import mark, raises
from rest_framework.test import APIClient

from control.models import ResponseFile
from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()


def get_response_file(user, id):
    return utils.get_resource(client, user, 'response-file', id)


def trash_response_file(user, id, payload):
    utils.login(client, user=user)
    url = reverse('response-file-trash', args=[id])
    response = client.put(url, payload)
    return response


########## Read methods : API endpoint closed.

def test_retrieve_API_is_closed():
    with raises(NoReverseMatch):
        response_file = factories.ResponseFileFactory()
        reverse('api:response-file-detail', args=[response_file.id])


def test_list_API_is_closed():
    with raises(NoReverseMatch):
        reverse('api:response-file-list')


########## write methods : API endpoints for create, update, patch and delete are closed.

def test_create_API_is_closed():
    with raises(NoReverseMatch):
        reverse('api:response-file-list')


def test_update_API_is_closed():
    with raises(NoReverseMatch):
        response_file = factories.ResponseFileFactory()
        reverse('api:response-file-detail', args=[response_file.id])
        # same url for patch and delete


########## trash

def test_cannot_trash_response_file_if_user_not_logged_in():
    response_file = factories.ResponseFileFactory()
    url = reverse('response-file-trash', args=[response_file.id])
    response = client.get(url)
    assert response.status_code == 403


def test_cannot_trash_response_file_if_control_is_not_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    payload = { "is_deleted": "true" }

    response = trash_response_file(user, response_file.id, payload)

    assert 400 <= response.status_code <= 499


def test_can_trash_response_file_if_control_is_associated_with_the_user():
    response_file = factories.ResponseFileFactory()
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }
    count_before = ResponseFile.objects.count()
    assert not ResponseFile.objects.get(id=response_file.id).is_deleted

    response = trash_response_file(user, response_file.id, payload)

    assert response.status_code == 200
    count_after = ResponseFile.objects.count()
    assert count_before == count_after
    assert ResponseFile.objects.get(id=response_file.id).is_deleted


def test_trashing_logs_an_action():
    response_file = factories.ResponseFileFactory()
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }
    assert not Action.objects.filter(verb__contains="trashed response-file").exists()
    trash_response_file(user, response_file.id, payload)
    assert Action.objects.filter(verb__contains="trashed response-file").exists()
    action = Action.objects.filter(verb__contains="trashed response-file").last()
    assert action.actor_object_id == str(user.id)
    assert action.target_object_id == str(response_file.id)


def test_trashing_moves_the_file_on_disk():
    response_file = factories.ResponseFileFactory()
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }

    path_before = response_file.file.path
    assert 'CORBEILLE' not in path_before

    trash_response_file(user, response_file.id, payload)

    path_after = ResponseFile.objects.get(id=response_file.id).file.path
    assert path_after != path_before
    assert 'CORBEILLE' in path_after


def test_trashing_keeps_the_same_basename():
    response_file = factories.ResponseFileFactory()
    basename_before = response_file.basename
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }

    trash_response_file(user, response_file.id, payload)

    basename_after = ResponseFile.objects.get(id=response_file.id).basename
    assert basename_after == basename_before


def test_cannot_retrash_a_trashed_file():
    response_file = factories.ResponseFileFactory(is_deleted=True)
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }

    response = trash_response_file(user, response_file.id, payload)

    assert 400 <= response.status_code < 500
    assert ResponseFile.objects.get(id=response_file.id).is_deleted


def test_cannot_untrash_a_file():
    response_file = factories.ResponseFileFactory(is_deleted=True)
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "false" }

    response = trash_response_file(user, response_file.id, payload)

    assert 400 <= response.status_code < 500
    assert ResponseFile.objects.get(id=response_file.id).is_deleted


def test_cannot_trash_response_file_if_control_is_deleted():
    response_file = factories.ResponseFileFactory()
    user = utils.make_audited_user(response_file.question.theme.questionnaire.control)
    payload = { "is_deleted": "true" }
    response_file.question.theme.questionnaire.control.delete()
    response = trash_response_file(user, response_file.id, payload)
    assert response.status_code == 404
