from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Questionnaire, Theme, Question
from control.serializers import QuestionnaireSerializer
from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


def get_questionnaire(user, id):
    return utils.get_resource(client, user, 'questionnaire', id)


def create_questionnaire(user, payload):
    return utils.create_resource(client, user, 'questionnaire', payload)


def update_questionnaire(user, payload):
    return utils.update_resource(client, user, 'questionnaire', payload)


def delete_questionnaire(user, id):
    return utils.delete_resource(client, user, 'questionnaire', id)


def make_create_payload(control_id):
    return {
        "title": "questionnaire questionnaire",
        "control": str(control_id),
        "is_draft": True,
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
    audited_user = utils.make_audited_user(questionnaire.control)

    # get
    assert get_questionnaire(audited_user, questionnaire.id).status_code == 200

    # create
    inspector_user = utils.make_inspector_user(questionnaire.control)
    payload = make_create_payload(questionnaire.control.id)
    assert create_questionnaire(inspector_user, payload).status_code == 201


def test_no_access_to_questionnaire_api_if_control_is_not_associated_with_the_user():
    questionnaire_in = factories.QuestionnaireFactory()
    questionnaire_out = factories.QuestionnaireFactory()
    assert questionnaire_in.control.id != questionnaire_out.control.id
    user = utils.make_inspector_user(questionnaire_in.control)

    # get
    assert get_questionnaire(user, questionnaire_out.id).status_code != 200

    # create
    payload = make_create_payload(questionnaire_out.control.id)
    clear_saved_data()
    assert create_questionnaire(user, payload).status_code != 201
    assert_no_data_is_saved()


def test_no_access_to_questionnaire_api_for_anonymous():
    questionnaire = factories.QuestionnaireFactory()

    # get
    response = utils.get_resource_without_login(client, 'questionnaire', questionnaire.id)
    assert response.status_code == 403

    # update
    payload = make_update_payload(questionnaire)
    response = utils.update_resource_without_login(client, 'questionnaire', payload)
    assert response.status_code == 403

    # delete
    response = utils.delete_resource_without_login(client, 'questionnaire', questionnaire.id)
    assert response.status_code == 403

    # create
    clear_saved_data()
    payload = make_create_payload(questionnaire.control.id)
    response = utils.create_resource_without_login(client, 'questionnaire', payload)
    assert response.status_code == 403
    assert_no_data_is_saved()


def test_no_modifying_questionnaire_if_not_inspector():
    questionnaire = factories.QuestionnaireFactory()
    audited_user = utils.make_audited_user(questionnaire.control)

    # update
    payload = make_update_payload(questionnaire)
    assert update_questionnaire(audited_user, payload).status_code == 403

    # delete
    assert delete_questionnaire(audited_user, questionnaire.id).status_code == 403

    # create
    clear_saved_data()
    payload = make_create_payload(questionnaire.control.id)
    assert create_questionnaire(audited_user, payload).status_code == 403
    assert_no_data_is_saved()


def test_no_access_to_draft_if_not_inspector():
    questionnaire = factories.QuestionnaireFactory(is_draft=True)
    audited_user = utils.make_audited_user(questionnaire.control)

    assert get_questionnaire(audited_user, questionnaire.id).status_code != 200


def test_questionnaire_create__success():
    increment_ids()
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload(control.id)
    # Before test, no saved data
    assert_no_data_is_saved()

    response = create_questionnaire(user, payload)
    assert 200 <= response.status_code < 300

    # Response.data is filled in
    questionnaire = response.data
    assert questionnaire['id'] > -1
    assert questionnaire['is_draft'] == True

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
    assert questionnaire.is_draft == True

    assert Theme.objects.all().count() == 1
    theme = Theme.objects.get(id=response.data['themes'][0]['id'])  # should not throw
    assert theme.questionnaire == questionnaire

    assert Question.objects.all().count() == 1
    question = Question.objects.get(id=response.data['themes'][0]['questions'][0]['id'])  # should not throw
    assert question.theme == theme


def test_questionnaire_create_fails_without_control_id():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload(control.id)

    # No control field : malformed request
    payload.pop('control')
    response = create_questionnaire(user, payload)
    assert response.status_code == 400

    # "control" : "null" : malformed request
    payload['control'] = None
    response = create_questionnaire(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()

    # "control" : "" : malformed request
    payload['control'] = ""
    response = create_questionnaire(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


def test_questionnaire_create_fails_with_malformed_theme():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload(control.id)

    payload['themes'][0].pop('title')
    response = create_questionnaire(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


def test_questionnaire_create_fails_with_malformed_question():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload(control.id)

    payload['themes'][0]['questions'][0].pop('description')
    response = create_questionnaire(user, payload)
    assert response.status_code == 400
    assert_no_data_is_saved()


# Create questionnaire draft through api, to set the editor properly.
def create_questionnaire_through_api(user, control):
    payload = make_create_payload(control.id)
    payload['is_draft'] = True
    response = create_questionnaire(user, payload)
    assert 200 <= response.status_code < 300
    return response.data


def test_questionnaire_draft_update__editor_can_update():
    increment_ids()
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    questionnaire = create_questionnaire_through_api(user, control)

    payload = questionnaire
    payload['description'] = 'this is a great questionnaire.'

    response = update_questionnaire(user, payload)
    assert response.status_code == 200


def test_questionnaire_draft_update__non_editor_cannot_update():
    increment_ids()
    questionnaire = factories.QuestionnaireFactory()
    control = questionnaire.control
    non_editor = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    payload = make_update_payload(questionnaire)
    payload['description'] = 'this is a great questionnaire.'
    response = update_questionnaire(non_editor, payload)
    assert 400 <= response.status_code < 500


def test_questionnaire_update__questionnaire_update():
    increment_ids()
    # Qr with no themes or questions.
    questionnaire = factories.QuestionnaireFactory()
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['description'] = 'this is a great questionnaire.'
    payload['is_draft'] = False

    assert Questionnaire.objects.all().count() == 1
    assert payload['description'] != questionnaire.description

    response = update_questionnaire(user, payload)
    assert response.status_code == 200

    # Data is saved
    assert Questionnaire.objects.all().count() == 1
    saved_qr = Questionnaire.objects.get(id=questionnaire.id)
    assert saved_qr.description != questionnaire.description
    assert saved_qr.description == payload['description']
    assert saved_qr.is_draft == False


def test_questionnaire_update__theme_update():
    increment_ids()
    theme = factories.ThemeFactory()
    questionnaire = theme.questionnaire
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['themes'][0]['title'] = 'this is a great theme.'

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert payload['themes'][0]['title'] != theme.title

    response = update_questionnaire(user, payload)
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
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)
    payload['themes'].append(added_theme)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    response = update_questionnaire(user, payload)
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
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'][0]['description'] = 'this is a great question.'

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
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
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'].append(added_question)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
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


def test_questionnaire_delete():
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = utils.make_inspector_user(questionnaire.control)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = delete_questionnaire(user, questionnaire.id)
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
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'][0]['questions'] = []

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    assert Question.objects.all().count() == 0

    # Response data is filled in
    assert len(response.data['themes'][0].get('questions', [])) == 0


def test_questionnaire_update__theme_delete():
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    payload['themes'] = []

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 0
    assert Question.objects.all().count() == 0

    # Response data is filled in
    assert len(response.data.get('themes', [])) == 0


def run_test_questionnaire_update__question_recreated(modify_payload_func):
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    original_id = payload['themes'][0]['questions'][0]['id']
    modify_payload_func(payload)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1

    assert Question.objects.all().count() == 1
    # Original question was deleted
    assert Question.objects.all().last().id != original_id

    # Response data is filled in
    assert len(response.data['themes'][0].get('questions', [])) == 1


def test_questionnaire_update__question_recreated_if_no_id():
    def modify_payload(payload):
        payload['themes'][0]['questions'][0].pop('id')

    run_test_questionnaire_update__question_recreated(modify_payload)


def run_test_questionnaire_update__theme_recreated(modify_payload_func):
    increment_ids()
    question = factories.QuestionFactory()
    theme = question.theme
    questionnaire = theme.questionnaire
    user = utils.make_inspector_user(questionnaire.control)
    payload = make_update_payload(questionnaire)

    original_id = payload['themes'][0]['id']
    modify_payload_func(payload)

    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    response = update_questionnaire(user, payload)
    assert response.status_code == 200

    # data is saved
    assert Questionnaire.objects.all().count() == 1
    assert Theme.objects.all().count() == 1
    assert Question.objects.all().count() == 1

    # Original theme was deleted
    assert Theme.objects.all().last().id != original_id

    # Response data is filled in
    assert len(response.data.get('themes', [])) == 1
    assert len(response.data['themes'][0].get('questions', [])) == 1


def test_questionnaire_update__theme_recreated_if_no_id():
    def modify_payload(payload):
        payload['themes'][0].pop('id')

    run_test_questionnaire_update__theme_recreated(modify_payload)


def test_questionnaire_update__theme_recreated_if_bad_id():
    bad_id = 123456

    def modify_payload(payload):
        good_id = payload['themes'][0]['id']
        assert good_id != bad_id
        payload['themes'][0]['id'] = bad_id

    run_test_questionnaire_update__theme_recreated(modify_payload)

    # The new theme and question has a new id.
    assert Theme.objects.all().last().id != bad_id
