from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


class SendResponseFileRunner:
    def __init__(self, client):
        response_file = factories.ResponseFileFactory()
        self.filename = response_file.basename
        user = response_file.author
        user.profile.controls.add(response_file.question.theme.questionnaire.control)
        user.profile.agreed_to_tos = True
        user.profile.save()
        utils.login(client, user=response_file.author)
        url = reverse('send-response-file', args=[response_file.id])
        self.response = client.get(url)


def test_download_response_file_works_if_the_control_is_associated_with_the_user(client):
    runner = SendResponseFileRunner(client)
    assert runner.response.status_code == 200


def test_download_response_file_has_right_filename(client):
    runner = SendResponseFileRunner(client)
    assert runner.response.has_header('Content-Disposition')
    assert runner.response['Content-Disposition'].find(runner.filename) > -1


def test_download_response_file_fails_if_the_control_is_not_associated_with_the_user(client):
    response_file = factories.ResponseFileFactory()
    user = response_file.author
    unauthorized_control = factories.ControlFactory()
    assert unauthorized_control != response_file.question.theme.questionnaire.control
    user.profile.controls.add(unauthorized_control)
    user.profile.save()
    utils.login(client, user=response_file.author)
    url = reverse('send-response-file', args=[response_file.id])
    response = client.get(url)
    assert response.status_code != 200
