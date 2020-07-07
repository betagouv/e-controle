from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


def test_download_response_file_list_works_if_the_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    user = utils.make_audited_user(questionnaire.control)
    utils.login(client, user=user)
    url = reverse('send-response-file-list', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code == 200


def test_download_response_file_list_fails_if_the_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    unauthorized_control = factories.ControlFactory()
    user = utils.make_audited_user(unauthorized_control)
    utils.login(client, user=user)
    url = reverse('send-response-file-list', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code != 200
