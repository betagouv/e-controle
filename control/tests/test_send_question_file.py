from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


def test_download_question_file_has_right_filename(client):
    question_file = factories.QuestionFileFactory()
    filename = question_file.basename

    user = factories.UserFactory()
    user.profile.controls.add(question_file.question.theme.questionnaire.control)
    user.profile.save()

    utils.login(client, user=user)
    url = reverse('send-question-file', args=[question_file.id])
    response = client.get(url)

    assert response['Content-Disposition'].find(filename) > -1


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
