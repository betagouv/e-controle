from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient

from control.models import QuestionFile, Questionnaire
from tests import factories, utils
from user_profiles.models import UserProfile

pytestmark = mark.django_db
client = APIClient()

User = get_user_model()


## List API

def test_inspector_can_list_question_file_from_draft_questionnaire():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    questionnaire = question_file.question.theme.questionnaire
    inspector.controls.add(questionnaire.control)
    draft_question_file = factories.QuestionFileFactory()
    draft_questionnaire = draft_question_file.question.theme.questionnaire
    draft_questionnaire.is_draft = True
    draft_questionnaire.save()
    inspector.controls.add(draft_questionnaire.control)
    assert not Questionnaire.objects.get(id=questionnaire.id).is_draft
    assert Questionnaire.objects.get(id=draft_questionnaire.id).is_draft
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-list')
    response = client.get(url)
    assert question_file.file.name in str(response.content)
    assert draft_question_file.file.name in str(response.content)


def test_audited_cannot_list_question_file_from_draft_questionnaire():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    questionnaire = question_file.question.theme.questionnaire
    audited.controls.add(questionnaire.control)
    draft_question_file = factories.QuestionFileFactory()
    draft_questionnaire = draft_question_file.question.theme.questionnaire
    draft_questionnaire.is_draft = True
    draft_questionnaire.save()
    audited.controls.add(draft_questionnaire.control)
    assert not Questionnaire.objects.get(id=questionnaire.id).is_draft
    assert Questionnaire.objects.get(id=draft_questionnaire.id).is_draft
    utils.login(client, user=audited.user)
    url = reverse('api:annexe-list')
    response = client.get(url)
    assert question_file.file.name in str(response.content)
    assert draft_question_file.file.name not in str(response.content)


### Retrive API endpoint closed.


def get_question_file(user, id):
    return utils.get_resource(client, user, 'annexe', id)


def update_question_file(user, payload):
    return utils.update_resource(client, user, 'annexe', payload)


def test_cannot_get_question_file_even_if_user_belongs_to_control():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    inspector.controls.add(question_file.question.theme.questionnaire.control)
    audited.controls.add(question_file.question.theme.questionnaire.control)
    assert not question_file.question.theme.questionnaire.is_draft

    # method not allowed
    assert get_question_file(inspector.user, question_file.id).status_code == 405
    assert get_question_file(audited.user, question_file.id).status_code == 405


def test_cannot_get_inexistant_question_file():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)

    # method not allowed
    assert get_question_file(inspector.user, 21038476187629481736498376).status_code == 405


def test_cannot_get_question_file_if_control_is_deleted():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    inspector.controls.add(question_file.question.theme.questionnaire.control)
    question_file.question.theme.questionnaire.control.delete()

    # method not allowed
    assert get_question_file(inspector.user, question_file.id).status_code == 405


def test_audited_cannot_get_question_file_from_draft_questionnaire():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    audited.controls.add(question_file.question.theme.questionnaire.control)
    question_file.question.theme.questionnaire.is_draft = True
    question_file.question.theme.questionnaire.save()
    assert Questionnaire.objects.get(id=question_file.question.theme.questionnaire.id).is_draft

    # method not allowed
    assert get_question_file(audited.user, question_file.id).status_code == 405


def test_inspector_cannot_update_question_file_from_published_questionnaire():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    inspector.controls.add(question_file.question.theme.questionnaire.control)
    assert not question_file.question.theme.questionnaire.is_draft

    payload = {
        "id": question_file.id,
        "question": question_file.question.id + 1
    }

    # method not allowed
    assert update_question_file(inspector.user, payload).status_code == 405


def test_audited_cannot_update_question_file_from_published_questionnaire():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    audited.controls.add(question_file.question.theme.questionnaire.control)
    assert not question_file.question.theme.questionnaire.is_draft

    payload = {
        "id": question_file.id,
        "question": question_file.question.id + 1
    }

    # forbidden
    assert update_question_file(audited.user, payload).status_code == 403


def test_audited_cannot_update_question_file_from_draft_questionnaire():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    audited.controls.add(question_file.question.theme.questionnaire.control)
    question_file.question.theme.questionnaire.is_draft = True
    question_file.question.theme.questionnaire.save()
    assert Questionnaire.objects.get(id=question_file.question.theme.questionnaire.id).is_draft

    payload = {
        "id": question_file.id,
        "question": question_file.question.id + 1
    }

    # Forbidden
    assert update_question_file(audited.user, payload).status_code == 403


### Upload API
def test_inspector_can_upload_question_file():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question = factories.QuestionFactory()
    questionnaire = question.theme.questionnaire
    questionnaire.is_draft = True
    questionnaire.save()
    inspector.controls.add(questionnaire.control)
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


def test_inspector_cannot_upload_question_file_to_published_questionnaire():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question = factories.QuestionFactory()
    questionnaire = question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    inspector.controls.add(questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-list')
    count_before = QuestionFile.objects.count()

    post_data = {
        'file': factories.dummy_file.open(),
        'question': [question.id]
    }
    response = client.post(url, post_data, format='multipart')

    assert response.status_code == 403
    count_after = QuestionFile.objects.count()
    assert count_after == count_before


def test_inspector_can_remove_question_file():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    questionnaire = question_file.question.theme.questionnaire
    questionnaire.is_draft = True
    questionnaire.save()
    inspector.controls.add(questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-detail', args=[question_file.id])
    count_before = QuestionFile.objects.count()

    response = client.delete(url)

    assert response.status_code == 204
    count_after = QuestionFile.objects.count()
    assert count_after == count_before - 1


def test_inspector_cannot_remove_question_file_if_control_is_published():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    questionnaire = question_file.question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    inspector.controls.add(questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-detail', args=[question_file.id])
    count_before = QuestionFile.objects.count()

    response = client.delete(url)

    assert response.status_code == 403
    count_after = QuestionFile.objects.count()
    assert count_after == count_before


def test_inspector_cannot_remove_question_file_if_control_is_deleted():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question_file = factories.QuestionFileFactory()
    inspector.controls.add(question_file.question.theme.questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-detail', args=[question_file.id])
    count_before = QuestionFile.objects.count()
    question_file.question.theme.questionnaire.control.delete()

    response = client.delete(url)

    assert response.status_code == 404
    count_after = QuestionFile.objects.count()
    assert count_after == count_before


def test_cannot_upload_question_file_if_control_is_deleted():
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    question = factories.QuestionFactory()
    inspector.controls.add(question.theme.questionnaire.control)
    utils.login(client, user=inspector.user)
    url = reverse('api:annexe-list')
    post_data = {
        'file': factories.dummy_file.open(),
        'question': [question.id]
    }
    question.theme.questionnaire.control.delete()
    response = client.post(url, post_data, format='multipart')
    assert response.status_code == 403


def test_audited_cannot_upload_question_file():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question = factories.QuestionFactory()
    audited.controls.add(question.theme.questionnaire.control)
    utils.login(client, user=audited.user)
    url = reverse('api:annexe-list')
    count_before = QuestionFile.objects.count()

    post_data = {
        'file': factories.dummy_file.open(),
        'question': [question.id]
    }
    response = client.post(url, post_data, format='multipart')

    assert response.status_code == 403
    count_after = QuestionFile.objects.count()
    assert count_after == count_before


def test_audited_cannot_remove_question_file():
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    question_file = factories.QuestionFileFactory()
    audited.controls.add(question_file.question.theme.questionnaire.control)
    utils.login(client, user=audited.user)
    url = reverse('api:annexe-detail', args=[question_file.id])
    count_before = QuestionFile.objects.count()

    response = client.delete(url)

    assert response.status_code == 403
    count_after = QuestionFile.objects.count()
    assert count_after == count_before
