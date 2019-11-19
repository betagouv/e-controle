from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, CreateView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from actstream import action
from actstream.models import model_stream
from sendfile import sendfile
import json

from .docx import generate_questionnaire_file
from .models import Control, Questionnaire, QuestionFile, ResponseFile
from .serializers import ControlDetailControlSerializer, QuestionnaireSerializer, ControlDetailUserSerializer


class WithListOfControlsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Questionnaires are grouped by control:
        # we get the list of questionnaire from the list of controls
        control_list = Control.objects.filter(id__in=self.request.user.profile.controls.all()).order_by('-id')
        context['controls'] = control_list
        return context


class ControlDetail(LoginRequiredMixin, WithListOfControlsMixin, TemplateView):
    template_name = "ecc/control_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        control_list = context['controls']
        controls_serialized = []
        for control in control_list:
            control_serialized = ControlDetailControlSerializer(instance=control).data
            controls_serialized.append(control_serialized)
        context['controls_json'] = json.dumps(controls_serialized)
        user_serialized = ControlDetailUserSerializer(instance=self.request.user).data
        user_serialized['is_inspector'] = self.request.user.profile.is_inspector
        context['user_json'] = json.dumps(user_serialized)
        return context


class Trash(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    model = Questionnaire
    template_name = "ecc/trash.html"

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response_files = ResponseFile.objects \
            .filter(question__theme__questionnaire=self.get_object()) \
            .filter(is_deleted=True)

        response_file_ids = response_files.values_list('id', flat=True)

        stream = model_stream(ResponseFile)\
            .filter(verb='trashed response-file')\
            .filter(target_object_id__in=list(response_file_ids)) \
            .order_by('timestamp')

        response_file_list = []
        for action in stream:
            response_file = response_files.get(id=action.target_object_id)
            response_file.deletion_date = action.timestamp
            response_file.deletion_user = User.objects.get(id=action.actor_object_id)
            response_file.question_number = str(response_file.question.theme.numbering) + \
                                            '.' + str(response_file.question.numbering)
            response_file_list.append(response_file)
        response_file_list.sort(key=lambda x: x.question_number)
        context['response_file_list'] = response_file_list

        return context


class QuestionnaireDetail(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'

    def get(self, request, *args, **kwargs):
        # Before accessing the questionnaire, we log who's accessing it.
        self.add_access_log_entry()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaire_json'] = \
            json.dumps(QuestionnaireSerializer(instance=self.get_object()).data)
        return context

    def add_access_log_entry(self):
        questionnaire = self.get_object()
        action_details = {
            'sender': self.request.user,
            'verb': 'accessed questionnaire',
            'target': questionnaire,
        }
        action.send(**action_details)


class QuestionnaireEdit(LoginRequiredMixin, WithListOfControlsMixin, DetailView):
    template_name = "ecc/questionnaire_create.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        if not self.request.user.profile.is_inspector:
            return Control.objects.none()
        questionnaires = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all(),
            editor=self.request.user
        )
        return questionnaires


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

    def add_upload_action_log(self):
        action_details = {
            'sender': self.request.user,
            'verb': 'uploaded response-file',
            'action_object': self.object,
            'target': self.object.question,
        }
        action.send(**action_details)

    def form_valid(self, form):
        try:
            question_id = form.data['question_id']
        except KeyError:
            raise forms.ValidationError("Question ID was missing on file upload")
        self.object = form.save(commit=False)
        self.object.question_id = question_id
        self.object.author = self.request.user
        self.object.save()
        self.add_upload_action_log()
        data = {'status': 'success'}
        response = JsonResponse(data)
        return response

    def format_form_errors(self, form):
        error_message = ""
        for field in form.errors:
            error_message += form.errors[field]
        return error_message

    def form_invalid(self, form):
        data = {
            'status': 'error',
            'error': self.format_form_errors(form),
        }
        response = JsonResponse(data, status=400)
        return response


class SendFileMixin(SingleObjectMixin):
    """
    Inheriting classes should override :
    - model to specify the data type of the file. The model class should implement
      a basename property.
    - (optional) get_query_set() to restrict the accessible files.
    """
    model = None
    file_type = None

    # used in a View, this function overrides the View's GET request handler.
    def get(self, request, *args, **kwargs):
        # get the object fetched by SingleObjectMixin
        obj = self.get_object()
        self.add_access_log_entry(accessed_object=obj)
        return sendfile(request, obj.file.path, attachment=True, attachment_filename=obj.basename)

    def add_access_log_entry(self, accessed_object):
        verb = f'accessed {self.file_type}'
        if self.file_type == 'response-file' and accessed_object.is_deleted:
            verb = 'accessed trashed-response-file'
        action_details = {
            'sender': self.request.user,
            'verb': verb,
            'target': accessed_object,
        }
        action.send(**action_details)


class SendQuestionnaireFile(SendFileMixin, LoginRequiredMixin, View):
    model = Questionnaire
    file_type = 'questionnaire-file'

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
    file_type = 'question-file'

    def get_queryset(self):
        # The user should only have access to files that belong to the control
        # he was associated with. That's why we filter-out based on the user's
        # control.
        return self.model.objects.filter(
            question__theme__questionnaire__control__in=self.request.user.profile.controls.all())


class SendResponseFile(SendQuestionFile):
    model = ResponseFile
    file_type = 'response-file'
