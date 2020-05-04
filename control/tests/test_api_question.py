from django.urls.exceptions import NoReverseMatch
from pytest import mark, raises
from rest_framework.test import APIClient

from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


def get_question(user, id):
    return utils.get_resource(client, user, 'question', id)


def test_can_access_question_api_if_control_is_associated_with_the_user():
    question = factories.QuestionFactory()
    questionnaire = question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    user = utils.make_audited_user(questionnaire.control)
    assert get_question(user, question.id).status_code == 200


def test_no_access_to_question_api_if_control_is_not_associated_with_the_user():
    question_in = factories.QuestionFactory()
    question_out = factories.QuestionFactory()
    user = utils.make_audited_user(question_in.theme.questionnaire.control)
    assert get_question(user, question_out.id).status_code != 200


def test_no_access_to_question_api_for_anonymous():
    question = factories.QuestionFactory()
    response = utils.get_resource_without_login(client, 'question', question.id)
    assert response.status_code == 403


def test_audited_cannot_get_a_question_if_questionnaire_is_draft():
    question = factories.QuestionFactory()
    user = utils.make_audited_user(question.theme.questionnaire.control)
    response = get_question(user, question.id)
    assert 400 <= response.status_code < 500


def test_response_file_listed_in_question_endpoint():
    response_file = factories.ResponseFileFactory()
    question = response_file.question
    user = response_file.author
    user.profile.agreed_to_tos = True
    user.profile.controls.add(question.theme.questionnaire.control)
    user.profile.save()

    response = get_question(user, question.id)
    assert response_file.basename in str(response.content)


def test_no_access_to_question_api_for_deleted_control():
    question = factories.QuestionFactory()
    user = utils.make_audited_user(question.theme.questionnaire.control)
    question.theme.questionnaire.control.delete()
    assert get_question(user, question.id).status_code == 404


def test_cannot_list_questions():
    with raises(NoReverseMatch):
        utils.list_resource_without_login(client, 'question')
