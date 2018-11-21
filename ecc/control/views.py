from django.views.generic import ListView


from .models import Questionnaire


class QuestionnaireList(ListView):
    template_name = "ecc/questionnaire_list.html"
    context_object_name = 'questionnaires'

    def get_queryset(self):
        return Questionnaire.objects.filter(control=self.kwargs.get('control_id'))


questionnaire_list = QuestionnaireList.as_view()
