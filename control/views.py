from django import forms
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import DetailView, CreateView, RedirectView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from actstream import action
from sendfile import sendfile

from control.questionnaire_duplicate import QuestionnaireDuplicateMixin
from .docx import generate_questionnaire_file
from .models import Questionnaire, QuestionFile, ResponseFile, Control


class WithListOfControlsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Questionnaires are grouped by control:
        # we get the list of questionnaire from the list of controls
        control_list = Control.objects.filter(id__in=self.request.user.profile.controls.all()).order_by('id')
        context['controls'] = control_list
        return context


class QuestionnaireList(LoginRequiredMixin, WithListOfControlsMixin, TemplateView):
    template_name = "ecc/questionnaire_list.html"


class QuestionnaireDetail(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset


class QuestionnaireEdit(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    template_name = "ecc/questionnaire_create.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        if not self.request.user.profile.is_inspector:
            return Control.objects.none()
        return Questionnaire.objects.filter(control__in=self.request.user.profile.controls.all())


class QuestionnaireCreate(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    """
    Creates a questionnaire on a given control (pk of control passed in URL).
    """
    template_name = "ecc/questionnaire_create.html"
    context_object_name = 'control'

    def get_queryset(self):
        if not self.request.user.profile.is_inspector:
            return Control.objects.none()
        return Control.objects.filter(id__in=self.request.user.profile.controls.all())


class FAQ(LoginRequiredMixin, WithListOfControlsMixin, TemplateView):
    template_name = "ecc/faq.html"


class UploadResponseFile(LoginRequiredMixin, CreateView):
    model = ResponseFile
    fields = ('file',)

    def form_valid(self, form):
        try:
            question_id = form.data['question_id']
        except KeyError:
            raise forms.ValidationError("Question ID was missing on file upload")
        self.object = form.save(commit=False)
        self.object.question_id = question_id
        self.object.author = self.request.user
        self.object.save()
        action_details = {
            'sender': self.request.user,
            'verb': 'uploaded',
            'action_object': self.object,
            'target': self.object.question,
        }
        action.send(**action_details)
        data = {'status': 'success'}
        response = JsonResponse(data)
        return response


class SendFileMixin(SingleObjectMixin):
    """
    Inheriting classes should override :
    - model to specify the data type of the file. The model class should implement
      a basename property.
    - (optional) get_query_set() to restrict the accessible files.
    """
    model = None

    # used in a View, this function overrides the View's GET request handler.
    def get(self, request, *args, **kwargs):
        # get the object fetched by SingleObjectMixin
        obj = self.get_object()
        return sendfile(request, obj.file.path, attachment=True, attachment_filename=obj.basename)


class SendQuestionnaireFile(SendFileMixin, LoginRequiredMixin, View):
    model = Questionnaire

    def get(self, request, *args, **kwargs):
        """
        Before sending the questionnaire file, we generate it.
        This means that the file is geneated every time this view is called - tipically
        when the user downloads the file.
        """
        questionnaire = self.get_object()
        generate_questionnaire_file(questionnaire)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(control__in=self.request.user.profile.controls.all())


class SendQuestionFile(SendFileMixin, LoginRequiredMixin, View):
    model = QuestionFile

    def get_queryset(self):
        # The user should only have access to files that belong to the control
        # he was associated with. That's why we filter-out based on the user's
        # control.
        return self.model.objects.filter(
            question__theme__questionnaire__control__in=self.request.user.profile.controls.all())


class SendResponseFile(SendQuestionFile):
    model = ResponseFile


class QuestionnaireDetail(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class MegacontrolConfirm(QuestionnaireDuplicateMixin, QuestionnaireDetail):
    template_name = "ecc/megacontrol_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['controls_to_copy_to'] = self.get_controls_to_copy_to(self.object)
        return context


@method_decorator(staff_member_required, name='dispatch')
class Megacontrol(LoginRequiredMixin, QuestionnaireDuplicateMixin, SingleObjectMixin, RedirectView):
    url = '/admin/control/questionnaire/'
    model = Questionnaire

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset

    def get(self, *args, **kwargs):
        questionnaire = self.get_object()
        controls_to_copy_to = self.get_controls_to_copy_to(questionnaire)

        created_questionnaires = []
        for control_to_copy_to in controls_to_copy_to:
            created_questionnaire = self.copy_questionnaire(questionnaire, control_to_copy_to)
            created_questionnaires.append(created_questionnaire)

        message = 'Vous avez créé les questionnaires suivants : <ul>'
        for created_questionnaire in created_questionnaires:
            message += f'<li>'
            message += f'  <a href="/admin/control/questionnaire/{created_questionnaire.id}/change/">'
            message += f'    <b> {created_questionnaire.id} : {created_questionnaire} </b>'
            message += f'  </a>'
            message += f'  dans l\'espace <b>{ created_questionnaire.control }</b>'
            message += f'</li>'
        message += '</ul>'
        messages.success(self.request, mark_safe(message))

        return super().get(*args, **kwargs)
