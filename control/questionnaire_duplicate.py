from django.contrib import messages
from django.core.files import File
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.urls import reverse

from control.models import Control, Question, Questionnaire, QuestionFile, Theme


class QuestionnaireDuplicateMixin(object):

    def __copy_themes(self, original_questionnaire, new_questionnaire):
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

    # used for the save_as button in Questionnaire detail admin page.
    def save_model(self, request, obj, form, change):
        new_questionnaire = obj
        new_questionnaire.save()
        # Django always sends this '_saveasnew' flag when clicking "save as new
        if '_saveasnew' in request.POST:
            original_pk = resolve(request.path).kwargs['object_id']
            original_questionnaire = Questionnaire.objects.get(pk=original_pk)
            self.__copy_themes(original_questionnaire, new_questionnaire)

    def copy_questionnaire(self, existing_questionnaire, control_to_copy_to):
        existing_questionnaire_id = existing_questionnaire.id
        existing_questionnaire.id = None
        existing_questionnaire.control = control_to_copy_to
        existing_questionnaire.order = None
        existing_questionnaire.save()
        new_questionnaire_id = existing_questionnaire.id

        # Fetch again to get the full objects.
        existing_questionnaire = Questionnaire.objects.get(id=existing_questionnaire_id)
        new_questionnaire = Questionnaire.objects.get(id=new_questionnaire_id)

        self.__copy_themes(existing_questionnaire, new_questionnaire)

        return Questionnaire.objects.get(id=new_questionnaire_id)

    def get_controls_to_copy_to(self, questionnaire):
        return Control.objects.filter(title=questionnaire.control.title).exclude(id=questionnaire.control.id)

    def do_megacontrol(self, questionnaire):
        controls_to_copy_to = self.get_controls_to_copy_to(questionnaire)

        created_questionnaires = []
        for control_to_copy_to in controls_to_copy_to:
            created_questionnaire = self.copy_questionnaire(questionnaire, control_to_copy_to)
            created_questionnaires.append(created_questionnaire)

        return created_questionnaires

    # used for the megacontrol action button in Questionnaire list admin page.
    def megacontrol_admin_action(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request,
                              "Megacontrôle : selectionnez un seul questionnaire à la fois.",
                              level=messages.ERROR)
            return

        ids_of_questionnaires_to_copy = queryset.values_list('id', flat=True)
        questionnaire_id = ids_of_questionnaires_to_copy[0]  # todo deal with more than 1 questionnaire
        return HttpResponseRedirect(reverse('megacontrol-confirm', args=[questionnaire_id]))

    megacontrol_admin_action.short_description = \
        "Mégacontrôle : copier ce questionnaire dans tous les espaces de la procédure"
