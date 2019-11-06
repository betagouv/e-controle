from pytest import mark

from django.shortcuts import reverse

from control.tests import test_api_questionnaire
from tests import factories, utils
from tests.factories import ControlFactory
from user_profiles.models import UserProfile

pytestmark = mark.django_db


def access_questionnaire_page(client, page_name, is_control_associated_with_user, profile_type, is_draft=False):
    questionnaire = factories.QuestionnaireFactory(is_draft=is_draft)
    control = questionnaire.control
    if is_control_associated_with_user:
        user = utils.make_user(profile_type, control)
    else:
        user = utils.make_user(profile_type, None)

    utils.login(client, user=user)
    url = reverse(page_name, args=[questionnaire.id])
    response = client.get(url)
    return response


def access_control_page(client, page_name, is_control_associated_with_user, profile_type):
    control = factories.ControlFactory()
    if is_control_associated_with_user:
        user = utils.make_user(profile_type, control)
    else:
        user = utils.make_user(profile_type, None)

    utils.login(client, user=user)
    url = reverse(page_name, args=[control.id])
    response = client.get(url)
    return response


def test_can_access_questionnaire_page_if_control_is_associated_with_the_user(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-detail',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.AUDITED)
    assert response.status_code == 200


def test_can_access_to_questionnaire_page_if_questionnaire_is_draft_and_user_is_inspector(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-detail',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.INSPECTOR,
                                         is_draft=True)
    assert response.status_code == 200


def test_no_access_to_questionnaire_page_if_questionnaire_is_draft_and_user_is_not_inspector(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-detail',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.AUDITED,
                                         is_draft=True)
    assert response.status_code == 404


def test_no_access_to_questionnaire_page_if_control_is_not_associated_with_the_user(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-detail',
                                         is_control_associated_with_user=False,
                                         profile_type=UserProfile.AUDITED)
    assert response.status_code != 200


def test_can_access_questionnaire_create_page_if_control_is_associated_with_the_inspector_user(client):
    response = access_control_page(client,
                                   page_name='questionnaire-create',
                                   is_control_associated_with_user=True,
                                   profile_type=UserProfile.INSPECTOR)
    assert response.status_code == 200


def test_no_access_questionnaire_create_page_if_control_is_not_associated_with_the_inspector_user(client):
    response = access_control_page(client,
                                   page_name='questionnaire-create',
                                   is_control_associated_with_user=False,
                                   profile_type=UserProfile.INSPECTOR)
    assert 400 <= response.status_code < 500


def test_no_access_questionnaire_create_page_if_not_inspector_user(client):
    response = access_control_page(client,
                                   page_name='questionnaire-create',
                                   is_control_associated_with_user=True,
                                   profile_type=UserProfile.AUDITED)
    assert 400 <= response.status_code < 500


def test_can_access_questionnaire_edit_page_if_control_is_associated_with_the_inspector_user_and_user_is_editor(client):
    # Create questionnaire through API so that the editor is set properly.
    control = ControlFactory()
    user = utils.make_user(UserProfile.INSPECTOR, control)
    payload = test_api_questionnaire.make_create_payload(control.id)
    create_response = test_api_questionnaire.create_questionnaire(user, payload)
    assert create_response.status_code == 201
    questionnaire_id = create_response.data['id']

    utils.login(client, user=user)
    url = reverse('questionnaire-edit', args=[questionnaire_id])
    response = client.get(url)

    assert response.status_code == 200


def test_no_access_questionnaire_edit_page_if_user_is_not_author(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-edit',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.INSPECTOR)
    assert 400 <= response.status_code < 500


def test_no_access_questionnaire_edit_page_if_control_is_not_associated_with_the_inspector_user(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-edit',
                                         is_control_associated_with_user=False,
                                         profile_type=UserProfile.INSPECTOR)
    assert 400 <= response.status_code < 500


def test_no_access_questionnaire_edit_page_if_not_inspector_user(client):
    response = access_questionnaire_page(client,
                                         page_name='questionnaire-edit',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.AUDITED)
    assert 400 <= response.status_code < 500


def test_no_access_trash_page_if_control_is_not_associated_with_the_user(client):
    response = access_questionnaire_page(client,
                                         page_name='trash',
                                         is_control_associated_with_user=False,
                                         profile_type=UserProfile.AUDITED)
    assert 400 <= response.status_code < 500


def test_can_access_trash_page_if_control_is_associated_with_the_user(client):
    response = access_questionnaire_page(client,
                                         page_name='trash',
                                         is_control_associated_with_user=True,
                                         profile_type=UserProfile.AUDITED)
    assert response.status_code == 200
