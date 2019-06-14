from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db


def make_inspector_user(control=None):
    user_profile = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    if control is not None:
        user_profile.controls.add(control)
    user_profile.save()
    return user_profile.user


def make_audited_user(control=None):
    user_profile = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    if control is not None:
        user_profile.controls.add(control)
    user_profile.save()
    return user_profile.user


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


def test_can_access_questionnaire_page_if_control_is_associated_with_the_inspector_user(client):
    control = factories.ControlFactory()
    user = make_inspector_user(control)
    utils.login(client, user=user)
    url = reverse('questionnaire-create', args=[control.id])
    response = client.get(url)
    assert response.status_code == 200


def test_no_access_questionnaire_page_if_control_is_not_associated_with_the_inspector_user(client):
    control = factories.ControlFactory()
    user = make_inspector_user()  # not associated with control
    utils.login(client, user=user)
    url = reverse('questionnaire-create', args=[control.id])
    response = client.get(url)
    assert 400 <= response.status_code < 500


def test_no_access_questionnaire_page_if_not_inspector_user(client):
    control = factories.ControlFactory()
    user = make_audited_user(control)
    utils.login(client, user=user)
    url = reverse('questionnaire-create', args=[control.id])
    response = client.get(url)
    assert 400 <= response.status_code < 500
