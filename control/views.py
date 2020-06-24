import magic
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, CreateView, TemplateView
from django.views.generic.detail import SingleObjectMixin


from actstream import action
from actstream.models import model_stream
from sendfile import sendfile
import json

from .docx import generate_questionnaire_file
from .export_response_files import generate_response_file_list_in_xlsx
from .models import Control, Questionnaire, QuestionFile, ResponseFile, Question
from .serializers import ControlDetailUserSerializer
from .serializers import ControlSerializer, ControlDetailControlSerializer


class WithListOfControlsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Questionnaires are grouped by control:
        # we get the list of questionnaire from the list of controls
        user_controls = self.request.user.profile.controls.active()
        control_list = Control.objects.filter(id__in=user_controls).order_by('-id')
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
        user_controls = self.request.user.profile.controls.active()
        queryset = Questionnaire.objects.filter(control__in=user_controls)
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
        for act in stream:
            response_file = response_files.get(id=act.target_object_id)
            response_file.deletion_date = act.timestamp
            response_file.deletion_user = User.objects.get(id=act.actor_object_id)
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
        user_controls = self.request.user.profile.controls.active()
        queryset = Questionnaire.objects.filter(control__in=user_controls)
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        control = self.get_object().control
        context['control_json'] = json.dumps(ControlSerializer(instance=control).data)
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
        user_controls = self.request.user.profile.controls.active()
        questionnaires = Questionnaire.objects.filter(
            control__in=user_controls,
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
        user_controls = self.request.user.profile.controls.active()
        if not self.request.user.profile.is_inspector:
            return Control.objects.none()
        return Control.objects.filter(id__in=user_controls)


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

    def add_invalid_extension_log(self, invalid_extension):
        action_details = {
            'sender': self.request.user,
            'verb': 'uploaded invalid response-file extension',
            'target': self.object.question,
            'description': f'Detected invalid file extension: "{invalid_extension}"'
            }
        action.send(**action_details)

    def add_invalid_mime_type_log(self, invalid_mime_type):
        action_details = {
            'sender': self.request.user,
            'verb': 'uploaded invalid response-file',
            'target': self.object.question,
            'description': f'Detected invalid response-file mime type: "{invalid_mime_type}"'
            }
        action.send(**action_details)

    def file_extension_is_valid(self, extension):
        blacklist = settings.UPLOAD_FILE_EXTENSION_BLACKLIST
        if any(match.lower() == extension.lower() for match in blacklist):
            return False
        return True

    def file_mime_type_is_valid(self, mime_type):
        blacklist = settings.UPLOAD_FILE_MIME_TYPE_BLACKLIST
        if any(match.lower() in mime_type.lower() for match in blacklist):
            return False
        return True

    def form_valid(self, form):
        if not self.request.user.profile.is_audited:
            return HttpResponseForbidden("User is not authorized to access this ressource")
        try:
            question_id = form.data['question_id']
        except KeyError:
            return HttpResponseBadRequest("Question ID was missing on file upload")
        get_object_or_404(
            Question,
            pk=question_id,
            theme__questionnaire__in=self.request.user.profile.questionnaires
        )
        self.object = form.save(commit=False)
        self.object.question_id = question_id
        self.object.author = self.request.user
        file_object = self.object.file
        file_extension = os.path.splitext(file_object.name)[1]
        if not self.file_extension_is_valid(file_extension):
            self.add_invalid_extension_log(file_extension)
            return HttpResponseForbidden(
                f"Cette extension de fichier n'est pas autorisée : {file_extension}")
        mime_type = magic.from_buffer(file_object.read(2048), mime=True)
        if not self.file_mime_type_is_valid(mime_type):
            self.add_invalid_mime_type_log(mime_type)
            return HttpResponseForbidden(f"Ce type de fichier n'est pas autorisé: {mime_type}")
        MAX_SIZE_BYTES = 1048576 * settings.UPLOAD_FILE_MAX_SIZE_MB
        if file_object.file.size > MAX_SIZE_BYTES:
            return HttpResponseForbidden(
                f"La taille du fichier dépasse la limite autorisée "
                f"de {settings.UPLOAD_FILE_MAX_SIZE_MB}Mo.")
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
    - (optional) get_queryset() to restrict the accessible files.
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
        return self.request.user.profile.questionnaires


class SendQuestionFile(SendFileMixin, LoginRequiredMixin, View):
    model = QuestionFile
    file_type = 'question-file'

    def get_queryset(self):
        # The user should only have access to files that belong to the control
        # he was associated with. That's why we filter-out based on the user's
        # control.
        user_controls = self.request.user.profile.controls.active()
        return self.model.objects.filter(
            question__theme__questionnaire__control__in=user_controls)


class SendResponseFile(SendQuestionFile):
    model = ResponseFile
    file_type = 'response-file'


class SendResponseFileList(SingleObjectMixin, LoginRequiredMixin, View):
    model = Questionnaire

    def get_queryset(self):
        user_controls = self.request.user.profile.controls.active()
        queryset = Questionnaire.objects.filter(control__in=user_controls)
        queryset = queryset.filter(is_draft=False)
        return queryset

    def get(self, request, *args, **kwargs):
        questionnaire = self.get_object()
        try:
            file = generate_response_file_list_in_xlsx(questionnaire)
            self.add_log_entry(verb='xls file exported', questionnaire=questionnaire)
            return sendfile(
                request,
                file.name,
                attachment=True,
                attachment_filename=f'réponses_questionnaire_{questionnaire.numbering}.xlsx')
        except Exception as e:
            self.add_log_entry(
                verb='xls file export failed', questionnaire=questionnaire, description=e
            )
            os.remove(file.name)

    def add_log_entry(self, verb, questionnaire, description=""):
        action_details = {
            'description': description,
            'sender': self.request.user,
            'verb': verb,
            'action_object': questionnaire.control,
            'target': questionnaire
        }

        action.send(**action_details)
