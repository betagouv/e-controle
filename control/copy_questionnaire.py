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


# Func to add to admin if needed
def copy_questionnaire(existing_questionnaire_id, id_of_control_to_copy_to):
    existing_questionnaire = Questionnaire.objects.get(id=existing_questionnaire_id)
    control_to_copy_to = Control.objects.get(id=id_of_control_to_copy_to)

    existing_questionnaire.id = None
    existing_questionnaire.control = control_to_copy_to
    existing_questionnaire.order = None
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

            existing_question = Question.objects.get(id=existing_question_id)
            new_question = Question.objects.get(id=new_question_id)
            for question_file in existing_question.question_files.all():
                copy_question_file(question_file.id, new_question.id)


def find_ids_of_controls_to_copy_to(existing_control_id):
    """
    Find controls with the same title.
    """
    existing_control = Control.objects.get(id=existing_control_id)
    ids = list(Control.objects.filter(title=existing_control.title).values_list('id', flat=True))
    return list(filter(lambda x: (x != existing_control_id), ids))


# Func for megacontrole : run it once to set up the whole megacontrole
def copy_questionnaire_everywhere(existing_questionnaire_id):
    existing_questionnaire = Questionnaire.objects.get(id=existing_questionnaire_id)
    ids_of_controls_to_copy_to = find_ids_of_controls_to_copy_to(existing_questionnaire.control.id)

    for id_of_control_to_copy_to in ids_of_controls_to_copy_to:
        copy_questionnaire(existing_questionnaire_id, id_of_control_to_copy_to)

