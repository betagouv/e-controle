from pytest import mark

from django.shortcuts import reverse

from rest_framework.test import APIClient

from tests import factories, utils


pytestmark = mark.django_db
client = APIClient()


def test_can_access_question_api_if_control_is_associated_with_the_user():
    question = factories.QuestionFactory()
    user = factories.UserFactory()
    user.profile.control = question.theme.questionnaire.control
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('question-detail', args=[question.id])
    response = client.get(url)
    assert response.status_code == 200


def test_no_access_to_question_api_if_control_is_not_associated_with_the_user():
    question_in = factories.QuestionFactory()
    question_out = factories.QuestionFactory()
    user = factories.UserFactory()
    user.profile.control = question_in.theme.questionnaire.control
    utils.login(client, user=user)
    url = reverse('question-detail', args=[question_out.id])
    response = client.get(url)
    assert response.status_code != 200


def test_no_access_to_question_api_for_anonymous():
    question = factories.QuestionFactory()
    url = reverse('question-detail', args=[question.id])
    response = client.get(url)
    assert response.status_code == 403


def test_response_file_listed_in_question_endpoint():
    response_file = factories.ResponseFileFactory()
    user = response_file.author
    question = response_file.question
    user.profile.control = response_file.question.theme.questionnaire.control
    user.profile.save()
    utils.login(client, user=response_file.author)
    url = reverse('question-detail', args=[question.id])
    response = client.get(url)
    assert response_file.basename in str(response.content)
