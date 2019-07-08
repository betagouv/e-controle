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
