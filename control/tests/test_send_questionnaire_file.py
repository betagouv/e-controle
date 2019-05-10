from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


def test_download_questionnaire_file_works_if_the_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory()
    user = factories.UserFactory()
    user.profile.controls.add(questionnaire.control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-questionnaire-file', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code == 200


def test_download_questionnaire_file_has_right_filename(client):
    questionnaire = factories.QuestionnaireFactory()
    filename = questionnaire.basename

    user = factories.UserFactory()
    user.profile.controls.add(questionnaire.control)
    user.profile.save()
    utils.login(client, user=user)
    url = reverse('send-questionnaire-file', args=[questionnaire.id])
    response = client.get(url)

    assert response.has_header('Content-Disposition')
    assert response['Content-Disposition'].find(filename) > -1


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

