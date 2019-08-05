from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


class SendQuestionnaireRunner():
    def __init__(self, client):
        questionnaire = factories.QuestionnaireFactory()
        self.filename = questionnaire.basename

        user = utils.make_audited_user(questionnaire.control)

        utils.login(client, user=user)
        url = reverse('send-questionnaire-file', args=[questionnaire.id])

        self.response = client.get(url)


def test_download_questionnaire_file_works_if_the_control_is_associated_with_the_user(client):
    runner = SendQuestionnaireRunner(client)
    assert runner.response.status_code == 200


def test_download_questionnaire_file_has_right_filename(client):
    runner = SendQuestionnaireRunner(client)
    assert runner.response.has_header('Content-Disposition')
    assert runner.response['Content-Disposition'].find(runner.filename) > -1


def test_download_questionnaire_file_fails_if_the_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    unauthorized_control = factories.ControlFactory()
    assert unauthorized_control != questionnaire.control
    user = utils.make_audited_user(unauthorized_control)
    utils.login(client, user=user)
    url = reverse('send-questionnaire-file', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code != 200

