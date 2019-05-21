from pytest import mark

from django.shortcuts import reverse

from rest_framework.test import APIClient

from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()


def make_user(control):
    user = factories.UserFactory()
    user.profile.controls.add(control)
    user.profile.save()
    return user


#### Questionnaire API ####

def call_questionnaire_detail_api(user, id):
    utils.login(client, user=user)
    url = reverse('api:questionnaire-detail', args=[id])
    response = client.get(url)
    return response


def call_questionnaire_list_api(user, payload):
    utils.login(client, user=user)
    url = reverse('api:questionnaire-list')
    response = client.post(url, payload, format='json')
    return response


def make_payload(control_id):
    return {
        "title": "questionnaire questionnaire",
        "control": str(control_id),
        "themes": [
           {
              "title": "theme theme theme",
              "questions": [
                {
                  "description": "bliblibli"
                }
              ]
           }
        ]
    }


def test_can_access_questionnaire_api_if_control_is_associated_with_the_user():
    questionnaire = factories.QuestionnaireFactory()
    user = make_user(questionnaire.control)

    assert call_questionnaire_detail_api(user, questionnaire.id).status_code == 200

    payload = make_payload(questionnaire.control.id)
    assert call_questionnaire_list_api(user, payload).status_code == 201


def test_no_access_to_questionnaire_api_if_control_is_not_associated_with_the_user():
    questionnaire_in = factories.QuestionnaireFactory()
    questionnaire_out = factories.QuestionnaireFactory()
    assert questionnaire_in.control.id != questionnaire_out.control.id
    user = make_user(questionnaire_in.control)

    assert call_questionnaire_detail_api(user, questionnaire_out.id).status_code != 200

    payload = make_payload(questionnaire_out.control.id)
    assert call_questionnaire_list_api(user, payload).status_code != 201


def test_no_access_to_questionnaire_api_for_anonymous():
    question = factories.QuestionFactory()

    url = reverse('api:questionnaire-detail', args=[question.id])
    response = client.get(url)
    assert response.status_code == 403

    payload = make_payload(question.theme.questionnaire.control.id)
    url = reverse('api:questionnaire-list')
    response = client.post(url, payload, format='json')
    assert response.status_code == 403


def test_questionnaire_create_theme_and_questions_are_hydrated():
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)

    response = call_questionnaire_list_api(user, payload)
    assert 200 <= response.status_code < 300

    questionnaire = response.data
    assert questionnaire['id'] > -1

    theme = response.data['themes'][0]
    assert theme['id'] > -1
    assert theme['questionnaire'] == questionnaire['id']

    question = theme['questions'][0]
    assert question['id'] > -1
    assert question['theme'] == theme['id']


def test_questionnaire_create_fails_without_control_id():
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)

    # No control field : malformed request
    payload.pop('control')
    response = call_questionnaire_list_api(user, payload)
    assert response.status_code == 400

    # "control" : "null" : not allowed
    payload['control'] = None
    response = call_questionnaire_list_api(user, payload)
    assert response.status_code == 403


#### Question API ####

def call_question_api(user, id):
    utils.login(client, user=user)
    url = reverse('api:question-detail', args=[id])
    response = client.get(url)
    return response


def test_can_access_question_api_if_control_is_associated_with_the_user():
    question = factories.QuestionFactory()
    user = make_user(question.theme.questionnaire.control)
    assert call_question_api(user, question.id).status_code == 200


def test_no_access_to_question_api_if_control_is_not_associated_with_the_user():
    question_in = factories.QuestionFactory()
    question_out = factories.QuestionFactory()
    user = make_user(question_in.theme.questionnaire.control)
    assert call_question_api(user, question_out.id).status_code != 200


def test_no_access_to_question_api_for_anonymous():
    question = factories.QuestionFactory()
    url = reverse('api:question-detail', args=[question.id])
    response = client.get(url)
    assert response.status_code == 403


def test_response_file_listed_in_question_endpoint():
    response_file = factories.ResponseFileFactory()
    question = response_file.question
    user = response_file.author
    user.profile.controls.add(question.theme.questionnaire.control)
    user.profile.save()

    response = call_question_api(user, question.id)
    assert response_file.basename in str(response.content)
