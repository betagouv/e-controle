from django.core.files import File

from control.models import Control, Question, Questionnaire, QuestionFile, Theme


def copy_question_file(existing_question_file_id, id_of_question_to_copy_to):
    """
    Copy an existing QuestionFile and add it to a given question.
    """
    existing_question_file = QuestionFile.objects.get(id=existing_question_file_id)
    question_to_copy_to = Question.objects.get(id=id_of_question_to_copy_to)

    new_file = File(existing_question_file.file, name=existing_question_file.basename)
    new_question_file = QuestionFile.objects.create(file=new_file, question=question_to_copy_to)
    new_question_file.save()


def get_ids_of_questions_to_copy_to(existing_question_id):
    """
    Find questions with the same description.
    """
    existing_question = Question.objects.get(id=existing_question_id)
    ids = Question.objects.filter(description=existing_question.description).values_list('id', flat=True)
    return list(ids)


def copy_all_the_things(existing_question_file_id):
    """
    Copy the given QuestionFile to all Questions with same description as the given Question.
    """
    existing_question_id = QuestionFile.objects.get(id=existing_question_file_id).question_id

    ids_of_questions_to_copy_to = get_ids_of_questions_to_copy_to(existing_question_id)

    for id_of_question_to_copy_to in ids_of_questions_to_copy_to:
        copy_question_file(existing_question_file_id, id_of_question_to_copy_to)


def copyQuestionnaire(existing_questionnaire_id, id_of_control_to_copy_to):
    existing_questionnaire = Questionnaire.objects.get(id=existing_questionnaire_id)
    control_to_copy_to = Control.objects.get(id=id_of_control_to_copy_to)

    existing_questionnaire.id = None
    existing_questionnaire.control = control_to_copy_to
    # TODO order field is copied along
    existing_questionnaire.save()
    new_questionnaire_id = existing_questionnaire.id

    # Fetch again to get the full objects.
    existing_questionnaire = Questionnaire.objects.get(id=existing_questionnaire_id)
    new_questionnaire = Questionnaire.objects.get(id=new_questionnaire_id)

    for theme in existing_questionnaire.themes.all():
        existing_theme_id = theme.id
        theme.id = None
        theme.questionnaire = new_questionnaire
        theme.save()
        new_theme_id = theme.id

        existing_theme = Theme.objects.get(id=existing_theme_id)
        new_theme = Theme.objects.get(id=new_theme_id)
        for question in existing_theme.questions.all():
            existing_question_id = question.id
            question.id = None
            question.theme = new_theme
            question.save()
            new_question_id = question.id

