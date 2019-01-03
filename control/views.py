from django import forms
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin

from sendfile import sendfile

from .models import Questionnaire, Theme, ResponseFile


class QuestionnaireList(ListView):
    template_name = "ecc/questionnaire_list.html"
    context_object_name = 'questionnaires'

    def get_queryset(self):
        return Questionnaire.objects.filter(control=self.request.user.profile.control)


class QuestionnaireDetail(DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'
    model = Questionnaire

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_list = Theme.objects.root_nodes().filter(
            questionnaire=self.object)
        questionnaire_list = Questionnaire.objects.filter(control=self.request.user.profile.control)
        context['themes'] = theme_list
        context['questionnaires'] = questionnaire_list
        return context


class UploadResponseFile(CreateView):
    model = ResponseFile
    fields = ('file',)

    def form_valid(self, form):
        try:
            question_id = form.data['question_id']
        except KeyError:
            raise forms.ValidationError("Question ID was missing on file upload")
        self.object = form.save(commit=False)
        self.object.question_id = question_id
        self.object.save()
        data = {'status': 'success'}
        response = JsonResponse(data)
        return response


class SendFileMixin(SingleObjectMixin):
    model = None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return sendfile(request, obj.file.path)


class SendResponseFile(SendFileMixin, View):
    model = ResponseFile


upload_response_file = UploadResponseFile.as_view()
questionnaire_list = QuestionnaireList.as_view()
questionnaire_detail = QuestionnaireDetail.as_view()
send_response_file = SendResponseFile.as_view()
