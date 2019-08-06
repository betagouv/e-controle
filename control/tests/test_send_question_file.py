from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


class SendQuestionFileRunner:
    def __init__(self, client):
        question_file = factories.QuestionFileFactory()
        self.filename = question_file.basename

        user = utils.make_audited_user(question_file.question.theme.questionnaire.control)

        utils.login(client, user=user)
        url = reverse('send-question-file', args=[question_file.id])

        self.response = client.get(url)


def test_download_question_file_works_if_the_control_is_associated_with_the_user(client):
    runner = SendQuestionFileRunner(client)
    assert runner.response.status_code == 200


def test_download_question_file_has_right_filename(client):
    runner = SendQuestionFileRunner(client)
    assert runner.response.has_header('Content-Disposition')
    assert runner.response['Content-Disposition'].find(runner.filename) > -1


def test_download_question_file_fails_if_the_control_is_not_associated_with_the_user(client):
    question_file = factories.QuestionFileFactory()
    unauthorized_control = factories.ControlFactory()
    assert unauthorized_control != question_file.question.theme.questionnaire.control
    user = utils.make_audited_user(unauthorized_control)
    utils.login(client, user=user)
    url = reverse('send-question-file', args=[question_file.id])
    response = client.get(url)
    assert response.status_code != 200
