from pytest import mark

from django.shortcuts import reverse

from tests import factories, utils


pytestmark = mark.django_db


def get_response_list(client, user, questionnaire_id):
    utils.login(client, user=user)
    url = reverse('send-response-file-list', args=[questionnaire_id])
    return client.get(url)


####################
# Tests for access
####################

def test_send_response_file_list_works_for_audited_if_the_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    user = utils.make_audited_user(questionnaire.control)

    response = get_response_list(client, user, questionnaire.id)

    assert response.status_code == 200


def test_send_response_file_list_fails_for_audited_if_the_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    unauthorized_control = factories.ControlFactory()
    user = utils.make_audited_user(unauthorized_control)

    response = get_response_list(client, user, questionnaire.id)

    assert response.status_code != 200

def test_send_response_file_list_works_for_inspector_if_the_control_is_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    user = utils.make_inspector_user(questionnaire.control)

    response = get_response_list(client, user, questionnaire.id)

    assert response.status_code == 200


def test_send_response_file_list_fails_for_inspector_if_the_control_is_not_associated_with_the_user(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=False)
    unauthorized_control = factories.ControlFactory()
    user = utils.make_inspector_user(unauthorized_control)

    response = get_response_list(client, user, questionnaire.id)

    assert response.status_code != 200


def test_send_response_file_list_fails_for_draft_questionnaire_for_inspector(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=True)
    user = utils.make_inspector_user(questionnaire.control)
    utils.login(client, user=user)
    url = reverse('send-response-file-list', args=[questionnaire.id])
    response = client.get(url)
    assert response.status_code != 200


def test_send_response_file_list_fails_for_draft_questionnaire_for_audited(client):
    questionnaire = factories.QuestionnaireFactory(is_draft=True)
    user = utils.make_audited_user(questionnaire.control)

    response = get_response_list(client, user, questionnaire.id)

    assert response.status_code != 200


###################################
# Tests for contents of file list
###################################
# Decoding the xlsx file is too complicated, so we test the file list before it is written to file.
from control.export_response_files import get_files_for_export

def test_send_response_file_list_contains_file(client):
    response_file = factories.ResponseFileFactory(is_deleted=False)
    questionnaire = response_file.question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    assert not questionnaire.is_draft
    user = utils.make_audited_user(questionnaire.control)

    files = get_files_for_export(questionnaire)

    assert len(files) == 1
    assert files[0].file.name == response_file.file.name


def test_send_response_file_list_does_not_contain_deleted_file(client):
    response_file = factories.ResponseFileFactory(is_deleted=True)
    questionnaire = response_file.question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    assert not questionnaire.is_draft
    user = utils.make_audited_user(questionnaire.control)

    files = get_files_for_export(questionnaire)

    assert len(files) == 0


def test_send_response_file_list_has_files_in_order_of_creation_date(client):
    response_file_1 = factories.ResponseFileFactory(is_deleted=False)
    question = response_file_1.question
    response_file_2 = factories.ResponseFileFactory(question=question, is_deleted=False)
    assert response_file_1.question == response_file_2.question
    assert response_file_1.file.name != response_file_2.file.name
    assert response_file_1.created < response_file_2.created

    questionnaire = response_file_1.question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    assert not questionnaire.is_draft

    user = utils.make_audited_user(questionnaire.control)

    files = get_files_for_export(questionnaire)

    assert len(files) == 2
    assert files[0].file.name == response_file_1.file.name
    assert files[1].file.name == response_file_2.file.name
    assert files[0].created < files[1].created


def test_send_response_file_list_has_files_in_order_of_question_numbering(client):
    question_1 = factories.QuestionFactory()
    question_2 = factories.QuestionFactory(theme=question_1.theme)
    assert question_1.numbering < question_2.numbering

    response_file_3 = factories.ResponseFileFactory(question=question_2, is_deleted=False)
    response_file_1 = factories.ResponseFileFactory(question=question_1, is_deleted=False)
    response_file_2 = factories.ResponseFileFactory(question=question_1, is_deleted=False)
    assert response_file_1.file.name != response_file_2.file.name
    assert response_file_1.file.name != response_file_3.file.name
    assert response_file_2.file.name != response_file_3.file.name

    questionnaire = response_file_1.question.theme.questionnaire
    questionnaire.is_draft = False
    questionnaire.save()
    assert not questionnaire.is_draft

    user = utils.make_audited_user(questionnaire.control)

    files = get_files_for_export(questionnaire)

    assert len(files) == 3
    assert files[0].file.name == response_file_1.file.name
    assert files[1].file.name == response_file_2.file.name
    assert files[2].file.name == response_file_3.file.name


def test_send_response_file_list_does_not_contais_files_from_other_questionnaire(client):
    response_file_1 = factories.ResponseFileFactory(is_deleted=False)
    questionnaire_1 = response_file_1.question.theme.questionnaire
    questionnaire_1.is_draft = False
    questionnaire_1.save()
    assert not questionnaire_1.is_draft

    # Questionnaire 2 in same control as questionnaire 1
    questionnaire_2 = factories.QuestionnaireFactory(control=questionnaire_1.control)
    questionnaire_2.is_draft = False
    questionnaire_2.save()
    assert not questionnaire_2.is_draft
    theme_2 = factories.ThemeFactory(questionnaire=questionnaire_2)
    question_2 = factories.QuestionFactory(theme=theme_2)
    response_file_2 = factories.ResponseFileFactory(is_deleted=False, question=question_2)

    user = utils.make_audited_user(questionnaire_1.control)

    files = get_files_for_export(questionnaire_1)

    assert len(files) == 1
    assert files[0].file.name == response_file_1.file.name
