from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, CreateView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from actstream import action
from sendfile import sendfile

from .models import Questionnaire, QuestionFile, ResponseFile, Control


class WithListOfControlsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Questionnaires are grouped by control:
        # we get the list of questionnaire from the list of controls
        control_list = Control.objects.filter(id__in=self.request.user.profile.controls.all())
        context['controls'] = control_list
        return context


class QuestionnaireList(LoginRequiredMixin, WithListOfControlsMixin, TemplateView):
    template_name = "ecc/questionnaire_list.html"


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset


class QuestionnaireEdit(LoginRequiredMixin, DetailView):
    template_name = "ecc/questionnaire_create.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        if not self.request.user.profile.is_inspector:
            return Control.objects.none()
        return Questionnaire.objects.filter(control__in=self.request.user.profile.controls.all())


class QuestionnaireCreate(LoginRequiredMixin, DetailView):
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
    - model to specify the data type of the file. The model class should implement a basename property.
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
