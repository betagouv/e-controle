from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Control
from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


#### Theme API ####
def get_theme(user, id):
    return utils.get_resource(client, user, 'theme', id)

def test_can_access_theme_api_if_control_is_associated_with_the_user():
    theme = factories.ThemeFactory()
    user = utils.make_audited_user(theme.questionnaire.control)
    assert get_theme(user, theme.id).status_code == 200


def test_no_access_to_theme_api_if_control_is_not_associated_with_the_user():
    theme_in = factories.ThemeFactory()
    theme_out = factories.ThemeFactory()
    user = utils.make_audited_user(theme_in.questionnaire.control)
    assert get_theme(user, theme_out.id).status_code != 200


def test_no_access_to_theme_api_for_anonymous():
    theme = factories.ThemeFactory()
    response = utils.get_resource_without_login(client, 'theme', theme.id)
    assert response.status_code == 403


def test_can_update_theme_order():
    theme = factories.ThemeFactory()
    user = utils.make_audited_user(theme.questionnaire.control)
    original_order = theme.order
    new_order = 123
    assert new_order != original_order

    payload = {
        "id": str(theme.id),
        "order": str(new_order),
        "title": theme.title
    }

    response = utils.update_resource(client, user, 'theme', payload)

    assert response.status_code == 200
    assert response.data['order'] == str(new_order)


#### Question API ####

def get_question(user, id):
    return utils.get_resource(client, user, 'question', id)


def test_can_access_question_api_if_control_is_associated_with_the_user():
    question = factories.QuestionFactory()
    user = utils.make_audited_user(question.theme.questionnaire.control)
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


def test_response_file_listed_in_question_endpoint():
    response_file = factories.ResponseFileFactory()
    question = response_file.question
    user = response_file.author
    user.profile.agreed_to_tos = True
    user.profile.controls.add(question.theme.questionnaire.control)
    user.profile.save()

    response = get_question(user, question.id)
    assert response_file.basename in str(response.content)


#### Control API ####

### Get
def get_control(user, id):
    return utils.get_resource(client, user, 'control', id)


def test_can_access_control_get_api_if_control_is_associated_with_the_user():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert get_control(user, control.id).status_code == 200


def test_no_access_to_control_get_api_if_control_is_not_associated_with_the_user():
    control_in = factories.ControlFactory()
    control_out = factories.ControlFactory()
    user = utils.make_audited_user(control_in)
    assert get_control(user, control_out.id).status_code != 200


def test_no_access_to_control_get_api_for_anonymous():
    control = factories.ControlFactory()
    response = utils.get_resource_without_login(client, 'control', control.id)
    assert response.status_code == 403


### Create
def create_control(user, payload):
    return utils.create_resource(client, user, 'control', payload)


def make_create_payload():
    return {
        "title": "new control",
        "reference_code": "ABC_2019",
    }


def test_can_access_control_create_api_if_inspector_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    assert create_control(user, make_create_payload()).status_code == 201


def test_cannot_create_control_with_special_characters_in_reference_code():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    data = make_create_payload()
    data['reference_code'] = 'this/is/not/good!'
    assert create_control(user, data).status_code == 400


def test_no_access_to_control_create_api_if_not_inspector():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert create_control(user, make_create_payload()).status_code == 403


def test_no_access_to_control_create_api_for_anonymous():
    payload = make_create_payload()
    response = utils.create_resource_without_login(client, 'control', payload)
    assert response.status_code == 403


def test_creates_control_and_adds_to_current_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload()
    response = create_control(user, payload)
    response_control = response.data

    # Response data
    assert response_control['title'] == payload['title']
    assert response_control['reference_code'] == payload['reference_code']

    # Saved data
    saved_control = Control.objects.get(id=response_control['id'])
    assert saved_control.title == payload['title']
    assert saved_control.reference_code == payload['reference_code']
    assert user.profile.controls.all().get(id=response_control['id']) == saved_control


### Update

def update_control(user, payload, control):
    utils.login(client, user=user)
    url = reverse('api:control-detail', args=[control.id])
    response = client.put(url, payload, format='json')
    return response


def make_update_payload():
    return {
        "title": "updated control",
        "depositing_organization": "updated organization",
    }


def test_can_access_control_update_api_if_inspector_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    assert update_control(user, make_update_payload(), control).status_code == 200


def test_no_access_to_control_update_api_if_not_inspector():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert update_control(user, make_update_payload(), control).status_code == 403


def test_inspector_cannot_update_a_control_that_does_not_belong_to_him():
    control1 = factories.ControlFactory()
    control2 = factories.ControlFactory()
    user = utils.make_inspector_user(control2)
    assert update_control(user, make_update_payload(), control1).status_code == 404


def test_no_access_to_control_update_api_for_anonymous():
    control = factories.ControlFactory()
    url = reverse('api:control-detail', args=[control.id])
    response = client.put(url, make_update_payload(), format='json')
    assert response.status_code == 403
