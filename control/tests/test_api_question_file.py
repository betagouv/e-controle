from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient

from control.models import QuestionFile
from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()

User = get_user_model()


def test_inspector_can_upload_question_file():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question = factories.QuestionFactory()
    inspector.controls.add(question.theme.questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-list')
    count_before = QuestionFile.objects.count()

    post_data = {
        'file': factories.dummy_file.open(),
        'question': [question.id]
    }
    response = client.post(url, post_data, format='multipart')

    assert response.status_code == 201
    count_after = QuestionFile.objects.count()
    assert count_after == count_before + 1


def test_inspector_can_remove_question_file():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    inspector.controls.add(question_file.question.theme.questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-detail', args=[question_file.id])
    count_before = QuestionFile.objects.count()

    response = client.delete(url)

    assert response.status_code == 204
    count_after = QuestionFile.objects.count()
    assert count_after == count_before - 1
