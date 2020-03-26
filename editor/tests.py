from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Questionnaire
from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()


def call_api(user, questionnaire_id, editor_id):
    utils.login(client, user=user)
    url = reverse('update-editor', args=[questionnaire_id])
    post_data = {
      'editor': editor_id
    }
    return client.put(url, post_data, format='json')


def assert_questionnaire_has_editor(questionnaire, user):
    assert Questionnaire.objects.get(id=questionnaire.id).editor == user


# Success cases

# the inspector resets themselves as editor on a draft questionnaire from a control they already edit.
# (not a real use case, but it's the most basic test)
def test_editor_can_reset_editor():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200
    assert_questionnaire_has_editor(questionnaire, user)


def test_noneditor_can_force_get_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    other_user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=other_user)
    assert_questionnaire_has_editor(questionnaire, other_user)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200
    assert_questionnaire_has_editor(questionnaire, user)


def test_editor_can_transfer_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    other_user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)

    response = call_api(user, questionnaire.id, other_user.id)

    assert response.status_code == 200
    assert_questionnaire_has_editor(questionnaire, other_user)


def test_editor_can_abandon_rights():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)

    response = call_api(user, questionnaire.id, None)

    assert response.status_code == 200
    assert_questionnaire_has_editor(questionnaire, None)


def test_noneditor_can_get_rights_on_questionnaire_without_editor():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=None)
    assert_questionnaire_has_editor(questionnaire, None)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200
    assert_questionnaire_has_editor(questionnaire, user)


# Fail cases

def test_audited_cannot_access_api():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500
    assert_questionnaire_has_editor(questionnaire, user)


def test_user_cannot_set_editor_if_they_cannot_access_the_questionnaire():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control=None, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500


def test_user_cannot_set_editor_if_questionnaire_is_not_draft():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=False)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500


# A query with no "editor" field in the JSON is a bad query, and will not unset the editor.
def test_query_without_editor_is_refused():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)

    utils.login(client, user=user)
    url = reverse('update-editor', args=[questionnaire.id])
    post_data = {
    }
    response = client.put(url, post_data, format='json')

    assert 400 <= response.status_code < 500
    assert_questionnaire_has_editor(questionnaire, user)


def test_no_access_to_editor_api_for_deleted_control():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)
    assert_questionnaire_has_editor(questionnaire, user)
    control.delete()
    response = call_api(user, questionnaire.id, user.id)
    assert response.status_code == 404