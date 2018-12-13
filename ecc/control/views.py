from django import forms
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView

from .models import Control, Questionnaire, Theme, ResponseFile, Question


class QuestionnaireList(ListView):
    template_name = "ecc/questionnaire_list.html"
    context_object_name = 'questionnaires'

    def get_queryset(self):
        control_id = Control.objects.first().id
        return Questionnaire.objects.filter(control=control_id)


class QuestionnaireDetail(DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'
    model = Questionnaire

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_list = Theme.objects.root_nodes().filter(
            questionnaire=self.object)
        context['themes'] = theme_list
        return context


class UploadResponseFileView(CreateView):
    model = ResponseFile
    fields = ('file',)

    def form_valid(self, form):
        try:
            numbering = form.data['question_bullet_number']
        except KeyError:
            raise forms.ValidationError("Question bullet number was missing on file upload")
        self.object = form.save(commit=False)
        self.object.question = Question.objects.first()
        self.object.question_numbering = numbering
        self.object.save()
        data = {'status': 'success'}
        response = JsonResponse(data)
        return response


upload_response_file = UploadResponseFileView.as_view()
questionnaire_list = QuestionnaireList.as_view()
questionnaire_detail = QuestionnaireDetail.as_view()
