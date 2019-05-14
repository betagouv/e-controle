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
