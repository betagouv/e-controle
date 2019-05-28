from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Control, Questionnaire, Theme, Question
from control.serializers import QuestionnaireSerializer
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


def call_questionnaire_create_api(user, payload):
    utils.login(client, user=user)
    url = reverse('api:questionnaire-list')
    response = client.post(url, payload, format='json')
    return response


def call_questionnaire_update_api(user, payload):
    utils.login(client, user=user)
    url = reverse('api:questionnaire-detail', args=[payload['id']])
    response = client.put(url, payload, format='json')
    return response


def call_questionnaire_delete_api(user, id):
    utils.login(client, user=user)
    url = reverse('api:questionnaire-detail', args=[id])
    response = client.delete(url)
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


def make_update_payload(questionnaire):
    serializer = QuestionnaireSerializer(instance=questionnaire)
    return serializer.data


def assert_no_data_is_saved():
    assert Questionnaire.objects.all().count() == 0
    assert Theme.objects.all().count() == 0
    assert Question.objects.all().count() == 0


def clear_saved_data():
    Questionnaire.objects.all().delete()
    Theme.objects.all().delete()
    Question.objects.all().delete()
    assert_no_data_is_saved()


def increment_ids():
    # We create objects for nothing, to increment ids. Otherwise question.id = theme.id = qr.id = 1, and some errors
    # are not detected.
    for _ in range(5):
        factories.ThemeFactory()
    for _ in range(5):
        factories.QuestionnaireFactory()
    clear_saved_data()


def test_can_access_questionnaire_api_if_control_is_associated_with_the_user():
    questionnaire = factories.QuestionnaireFactory()
    user = make_user(questionnaire.control)

    # get
    assert call_questionnaire_detail_api(user, questionnaire.id).status_code == 200

    # create
    payload = make_payload(questionnaire.control.id)
    assert call_questionnaire_create_api(user, payload).status_code == 201


def test_no_access_to_questionnaire_api_if_control_is_not_associated_with_the_user():
    questionnaire_in = factories.QuestionnaireFactory()
    questionnaire_out = factories.QuestionnaireFactory()
    assert questionnaire_in.control.id != questionnaire_out.control.id
    user = make_user(questionnaire_in.control)

    # get
    assert call_questionnaire_detail_api(user, questionnaire_out.id).status_code != 200

    # create
    payload = make_payload(questionnaire_out.control.id)
    clear_saved_data()
    assert call_questionnaire_create_api(user, payload).status_code != 201
    assert_no_data_is_saved()


def test_no_access_to_questionnaire_api_for_anonymous():
    question = factories.QuestionFactory()

    # get
    url = reverse('api:questionnaire-detail', args=[question.id])
    response = client.get(url)
    assert response.status_code == 403

    # create
    payload = make_payload(question.theme.questionnaire.control.id)
    clear_saved_data()
    url = reverse('api:questionnaire-list')
    response = client.post(url, payload, format='json')
    assert response.status_code == 403
    assert_no_data_is_saved()


def test_questionnaire_create__success():
    increment_ids()
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)
    # Before test, no saved data
    assert_no_data_is_saved()

    response = call_questionnaire_create_api(user, payload)
    assert 200 <= response.status_code < 300

    # Response.data is filled in
    questionnaire = response.data
    assert questionnaire['id'] > -1

    theme = response.data['themes'][0]
    assert theme['id'] > -1
    assert theme['questionnaire'] == questionnaire['id']

    question = theme['questions'][0]
    assert question['id'] > -1
    assert question['theme'] == theme['id']

    # Data is saved, foreign keys are set
    assert Questionnaire.objects.all().count() == 1
    questionnaire = Questionnaire.objects.get(id=response.data['id'])  # should not throw
    assert questionnaire.control == control

    assert Theme.objects.all().count() == 1
    theme = Theme.objects.get(id=response.data['themes'][0]['id'])  # should not throw
    assert theme.questionnaire == questionnaire

    assert Question.objects.all().count() == 1
    question = Question.objects.get(id=response.data['themes'][0]['questions'][0]['id'])  # should not throw
    assert question.theme == theme


def test_questionnaire_create_fails_without_control_id():
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)

    # No control field : malformed request
    payload.pop('control')
    response = call_questionnaire_create_api(user, payload)
    assert response.status_code == 400

    # "control" : "null" : malformed request
    payload['control'] = None
    response = call_questionnaire_create_api(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()

    # "control" : "" : malformed request
    payload['control'] = ""
    response = call_questionnaire_create_api(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


def test_questionnaire_create_fails_with_malformed_theme():
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)

    payload['themes'][0].pop('title')
    response = call_questionnaire_create_api(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


def test_questionnaire_create_fails_with_malformed_question():
    control = factories.ControlFactory()
    user = make_user(control)
    payload = make_payload(control.id)

    payload['themes'][0]['questions'][0].pop('description')
    response = call_questionnaire_create_api(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


def test_questionnaire_update__questionnaire_update():
    increment_ids()
    # Qr with no themes or questions.
    questionnaire = factories.QuestionnaireFactory()
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['description'] = 'this is a great questionnaire.'

    assert Questionnaire.objects.all().count() == 1
    assert payload['description'] != questionnaire.description

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # Data is saved
    assert Questionnaire.objects.all().count() == 1
    saved_qr = Questionnaire.objects.get(id=questionnaire.id)
    assert saved_qr.description != questionnaire.description
    assert saved_qr.description == payload['description']


def test_questionnaire_update__theme_update():
    increment_ids()
    theme = factories.ThemeFactory()
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['themes'][0]['title'] = 'this is a great theme.'

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert payload['themes'][0]['title'] != theme.title

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    saved_qr = Questionnaire.objects.get(id=questionnaire.id)
    assert saved_qr == questionnaire

    assert Theme.objects.all().count() == 1
    saved_theme = Theme.objects.get(id=theme.id)
    assert saved_theme.title != theme.title
    assert saved_theme.title == payload['themes'][0]['title']

    # Response data is filled in
    assert len(response.data['themes']) == 1
    assert response.data['themes'][0]['title'] == payload['themes'][0]['title']


def run_test_questionnaire_update__theme_create(added_theme):
    increment_ids()
    theme = factories.ThemeFactory()
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['themes'].append(added_theme)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    saved_qr = Questionnaire.objects.get(id=questionnaire.id)
    assert saved_qr == questionnaire

    assert Theme.objects.all().count() == 2
    new_theme = Theme.objects.last()
    assert new_theme.title == payload['themes'][1]['title']
    assert new_theme.questionnaire == saved_qr

    # Response data is filled in
    assert len(response.data['themes']) == 2
    assert response.data['themes'][1]['title'] == payload['themes'][1]['title']


def test_questionnaire_update__theme_create():
    added_theme = {'title': 'this is a great theme.' }
    run_test_questionnaire_update__theme_create(added_theme)


def test_questionnaire_update__theme_create_if_bad_id():
    added_theme = {
        'id': 123,  # id is bad. It should be ignored, so that this theme is considered new.
        'title': 'this is a great theme.'
    }
    run_test_questionnaire_update__theme_create(added_theme)

    # Id in payload was ignored and new id was assigned to the new theme
    new_theme = Theme.objects.last()
    assert new_theme.id != added_theme['id']


def test_questionnaire_update__question_update():
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'][0]['description'] = 'this is a great question.'

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # Data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    saved_question = Question.objects.get(id=question.id)
    assert saved_question.description != question.description
    assert saved_question.description == payload['themes'][0]['questions'][0]['description']

    # Response data is filled
    assert len(response.data['themes']) == 1
    assert len(response.data['themes'][0]['questions']) == 1
    assert \
        response.data['themes'][0]['questions'][0]['description'] == payload['themes'][0]['questions'][0]['description']


def run_test_questionnaire_update__question_create(added_question):
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'].append(added_question)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    assert Question.objects.all().count() == 2
    new_question = Question.objects.last()
    assert new_question.description == payload['themes'][0]['questions'][1]['description']

    # Response data is filled in
    assert len(response.data['themes'][0]['questions']) == 2
    assert \
        response.data['themes'][0]['questions'][1]['description'] == payload['themes'][0]['questions'][1]['description']


def test_questionnaire_update__question_create():
    added_question = {'description': 'this is a great question.'}
    run_test_questionnaire_update__question_create(added_question)


def test_questionnaire_update__question_create_if_bad_id():
    added_question = {
        'id': 123,  # id is bad. It should be ignored, so that this theme is considered new.
        'description': 'this is a great question.'
    }
    run_test_questionnaire_update__question_create(added_question)

    # Id in payload was ignored and new id was assigned to the new question
    new_question = Question.objects.last()
    assert new_question.id != added_question['id']


def test_questionnaire_delete():
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = call_questionnaire_delete_api(user, questionnaire.id)
    assert 200 <= response.status_code < 300

    # Cascade delete : child objects are deleted
    assert Questionnaire.objects.all().count() == 0
    assert Theme.objects.all().count() == 0
    assert Question.objects.all().count() == 0


def test_questionnaire_update__question_delete():
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = make_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'] = []

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = call_questionnaire_update_api(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    assert Question.objects.all().count() == 0

    # Response data is filled in
    assert len(response.data['themes'][0].get('questions', [])) == 0


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
