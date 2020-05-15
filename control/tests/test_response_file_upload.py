from pytest import mark

from django.shortcuts import reverse

from control.models import ResponseFile
from control.tests import test_api_questionnaire
from tests import factories, utils
from user_profiles.models import UserProfile


pytestmark = mark.django_db


def test_audited_can_upload_question_file(client):
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    audited.controls.add(question.theme.questionnaire.control)
    question.theme.questionnaire.is_draft = False
    question.theme.questionnaire.save()
    utils.login(client, user=audited.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_file.open(),
        'question_id': [question.id]
    }
    response = client.post(url, post_data, format='multipart')
    assert response.status_code == 200
    count_after = ResponseFile.objects.count()
    assert count_after == count_before + 1


def test_cannot_upload_question_file_if_control_is_deleted(client):
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    audited.controls.add(question.theme.questionnaire.control)
    question.theme.questionnaire.is_draft = False
    question.theme.questionnaire.save()
    utils.login(client, user=audited.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_file.open(),
        'question_id': [question.id]
    }
    question.theme.questionnaire.control.delete()
    response = client.post(url, post_data, format='multipart')
    assert 400 <= response.status_code < 500
    count_after = ResponseFile.objects.count()
    assert count_after == count_before


def test_audited_cannot_upload_question_file_if_questionnaire_is_draft(client):
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    audited.controls.add(question.theme.questionnaire.control)
    question.theme.questionnaire.is_draft = True
    question.theme.questionnaire.save()
    utils.login(client, user=audited.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_file.open(),
        'question_id': [question.id]
    }
    response = client.post(url, post_data, format='multipart')
    assert response.status_code == 404
    count_after = ResponseFile.objects.count()
    assert count_after == count_before


def test_cannot_upload_question_file_in_a_control_user_is_not_in(client):
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    assert question.theme.questionnaire.control not in audited.controls.active()
    question.theme.questionnaire.is_draft = False
    question.theme.questionnaire.save()
    utils.login(client, user=audited.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_file.open(),
        'question_id': [question.id]
    }
    response = client.post(url, post_data, format='multipart')
    assert 400 <= response.status_code < 500
    count_after = ResponseFile.objects.count()
    assert count_after == count_before


def test_inspector_cannot_upload_question_file(client):
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question = factories.QuestionFactory()
    inspector.controls.add(question.theme.questionnaire.control)
    question.theme.questionnaire.is_draft = False
    question.theme.questionnaire.save()
    utils.login(client, user=inspector.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_file.open(),
        'question_id': [question.id]
    }
    response = client.post(url, post_data, format='multipart')
    assert 400 <= response.status_code < 500
    count_after = ResponseFile.objects.count()
    assert count_after == count_before


def test_audited_cannot_upload_exe_file(client):
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    audited.controls.add(question.theme.questionnaire.control)
    question.theme.questionnaire.is_draft = False
    question.theme.questionnaire.save()
    utils.login(client, user=audited.user)
    url = reverse('response-upload')
    count_before = ResponseFile.objects.count()
    post_data = {
        'file': factories.dummy_exe_file.open(),
        'question_id': [question.id]
    }
    response = client.post(url, post_data, format='multipart')
    assert response.status_code == 403
    count_after = ResponseFile.objects.count()
    assert count_after == count_before
