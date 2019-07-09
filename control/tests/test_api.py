from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Control, Questionnaire, Theme, Question
from control.serializers import QuestionnaireSerializer
from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()


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


#### Question API ####

def call_question_api(user, id):
    utils.login(client, user=user)
    url = reverse('api:question-detail', args=[id])
    response = client.get(url)
    return response


def test_can_access_question_api_if_control_is_associated_with_the_user():
    question = factories.QuestionFactory()
    user = make_audited_user(question.theme.questionnaire.control)
    assert call_question_api(user, question.id).status_code == 200


def test_no_access_to_question_api_if_control_is_not_associated_with_the_user():
    question_in = factories.QuestionFactory()
    question_out = factories.QuestionFactory()
    user = make_audited_user(question_in.theme.questionnaire.control)
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


#### Control API ####

### Get
def call_control_get_api(user, id):
    utils.login(client, user=user)
    url = reverse('api:control-detail', args=[id])
    response = client.get(url)
    return response


def test_can_access_control_get_api_if_control_is_associated_with_the_user():
    control = factories.ControlFactory()
    user = make_audited_user(control)
    assert call_control_get_api(user, control.id).status_code == 200


def test_no_access_to_control_get_api_if_control_is_not_associated_with_the_user():
    control_in = factories.ControlFactory()
    control_out = factories.ControlFactory()
    user = make_audited_user(control_in)
    assert call_control_get_api(user, control_out.id).status_code != 200


def test_no_access_to_control_get_api_for_anonymous():
    control = factories.ControlFactory()
    url = reverse('api:control-detail', args=[control.id])
    response = client.get(url)
    assert response.status_code == 403


### Create
def call_control_create_api(user, payload):
    utils.login(client, user=user)
    url = reverse('api:control-list')
    response = client.post(url, payload, format='json')
    return response


def make_payload():
    return {
        "title": "new control",
        "reference_code": "ABC_2019",
    }


def test_can_access_control_create_api_if_inspector_user():
    control = factories.ControlFactory()
    user = make_inspector_user(control)
    assert call_control_create_api(user, make_payload()).status_code == 201


def test_no_access_to_control_create_api_if_not_inspector():
    control = factories.ControlFactory()
    user = make_audited_user(control)
    assert call_control_create_api(user, make_payload()).status_code == 403


def test_no_access_to_control_create_api_for_anonymous():
    control = factories.ControlFactory()
    url = reverse('api:control-list')
    response = client.post(url, make_payload(), format='json')
    assert response.status_code == 403


def test_creates_control_and_adds_to_current_user():
    control = factories.ControlFactory()
    user = make_inspector_user(control)
    payload = make_payload()
    response = call_control_create_api(user, payload)
    response_control = response.data

    # Response data
    assert response_control['title'] == payload['title']
    assert response_control['reference_code'] == payload['reference_code']

    # Saved data
    saved_control = Control.objects.get(id=response_control['id'])
    assert saved_control.title == payload['title']
    assert saved_control.reference_code == payload['reference_code']
    assert user.profile.controls.all().get(id=response_control['id']) == saved_control
