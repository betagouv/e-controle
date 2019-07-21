from django.core.files import File
from django.urls import resolve


from control.models import Question, Questionnaire, QuestionFile, Theme


class QuestionnaireDuplicateMixin(object):

    def save_model(self, request, obj, form, change):
        new_questionnaire = obj
        new_questionnaire.save()
        # Django always sends this '_saveasnew' flag when clicking "save as new
        if '_saveasnew' in request.POST:
            original_pk = resolve(request.path).kwargs['object_id']
            original_questionnaire = Questionnaire.objects.get(pk=original_pk)
            # original_themes = original_questionnaire.themes.all()
            # original_questions = original_theme.questions.all()
            for theme in original_questionnaire.themes.all():
                original_theme = Theme.objects.get(pk=theme.pk)
                theme.id = None
                theme.questionnaire = new_questionnaire
                theme.save()
                for question in original_theme.questions.all():
                    original_question = Question.objects.get(pk=question.pk)
                    question.id = None
                    question.theme = theme
                    question.save()
                    for question_file in original_question.question_files.all():
                        original_question_file = QuestionFile.objects.get(pk=question_file.pk)
                        new_file = File(
                            original_question_file.file, name=original_question_file.basename)
                        new_question_file = QuestionFile.objects.create(
                            file=new_file, question=question)
                        new_question_file.save()
