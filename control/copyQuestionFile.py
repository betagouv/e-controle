from django.core.files import File

from control.models import Question, QuestionFile


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

