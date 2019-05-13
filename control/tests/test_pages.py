from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


def test_can_access_questionnaire_page_if_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    user = factories.UserFactory()
    user.profile.controls.add(questionnaire.control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('questionnaire-detail', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code == 200


def test_no_access_to_questionnaire_page_if_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    user = factories.UserFactory()
    unautorized_control = factories.ControlFactory()
    assert unautorized_control != questionnaire.control
    user.profile.controls.add(unautorized_control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('questionnaire-detail', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code != 200


def test_download_questionnaire_file_works_if_the_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    user = factories.UserFactory()
    user.profile.controls.add(questionnaire.control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-questionnaire-file', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code == 200


def test_download_questionnaire_file_fails_if_the_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    user = factories.UserFactory()
    unautorized_control = factories.ControlFactory()
    assert unautorized_control != questionnaire.control
    user.profile.controls.add(unautorized_control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-questionnaire-file', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code != 200


def test_download_question_file_works_if_the_control_is_associated_with_the_user(client):
    question_file = factories.QuestionFileFactory()
    user = factories.UserFactory()
    user.profile.controls.add(question_file.question.theme.questionnaire.control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-question-file', args=[question_file.id])
    response = client.get(url)
    assert response.status_code == 200


def test_download_question_file_fails_if_the_control_is_not_associated_with_the_user(client):
    question_file = factories.QuestionFileFactory()
    user = factories.UserFactory()
    unautorized_control = factories.ControlFactory()
    assert unautorized_control != question_file.question.theme.questionnaire.control
    user.profile.controls.add(unautorized_control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-question-file', args=[question_file.id])
    response = client.get(url)
    assert response.status_code != 200


def test_download_response_file_works_if_the_control_is_associated_with_the_user(client):
    response_file = factories.ResponseFileFactory()
    user = response_file.author
    user.profile.controls.add(response_file.question.theme.questionnaire.control)
    user.profile.save()
    utils.login(client, user=response_file.author)
    url = reverse('send-response-file', args=[response_file.id])
    response = client.get(url)
    assert response.status_code == 200


def test_download_response_file_fails_if_the_control_is_not_associated_with_the_user(client):
    response_file = factories.ResponseFileFactory()
    user = response_file.author
    unautorized_control = factories.ControlFactory()
    assert unautorized_control != response_file.question.theme.questionnaire.control
    user.profile.controls.add(unautorized_control)
    user.profile.save()
    utils.login(client, user=response_file.author)
    url = reverse('send-response-file', args=[response_file.id])
    response = client.get(url)
    assert response.status_code != 200
