from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()

def call_api(user, questionnaire_id, editor_id):
    utils.login(client, user=user)
    url = reverse('update-editor', args=[questionnaire_id])
    post_data = {
      'editor': editor_id
    }
    return client.put(url, post_data, format='json')


def test_success():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control, assign_questionnaire_editor=False)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, user.id)

    assert response.status_code == 200

def test_audited_cannot_access():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    questionnaire = factories.QuestionnaireFactory(control=control, is_draft=True, editor=user)

    response = call_api(user, questionnaire.id, user.id)

    assert 400 <= response.status_code < 500

