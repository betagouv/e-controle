from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()

def call_api(user, questionnaire_id, editor_id):
    utils.login(client, user=user)
    url = reverse('update-editor', args=[questionnaire_id])
    post_data = {
      'editor': editor_id
    }
    return client.put(url, post_data, format='json')

# the inspector resets themselves as editor on a draft questionnaire from a control they already edit.
# (not a real use case, but it's the most basic test)
def test_success_reset():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200

def test_success_force_get_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    other_user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=other_user)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200

def test_success_transfer_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    other_user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, other_user.id)

    assert response.status_code == 200

def test_success_abandon_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, None)

    assert response.status_code == 200

def test_success_get_rights_on_unedited_questionnaire():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=None)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200


# todo check the saved questionnaire has a new editor


def test_fail_audited_cannot_access_api():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500

def test_fail_if_inspector_doesnt_own_questionnaire():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control=None, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500

def test_fail_if_questionnaire_not_draft():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=False)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500

# A query with no "editor" field in the JSON is a bad query, and will not unset the editor.
def test_fail_query_without_editor_is_refused():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    utils.login(client, user=user)
    url = reverse('update-editor', args=[questionnaire.id])
    post_data = {
    }
    response = client.put(url, post_data, format='json')

    assert 400 <= response.status_code < 500
