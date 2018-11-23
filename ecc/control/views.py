from django.views.generic import ListView, DetailView


from .models import Control, Questionnaire, Theme


class QuestionnaireList(ListView):
    template_name = "ecc/questionnaire_list.html"
    context_object_name = 'questionnaires'

    def get(self, request):
        request.session['user_profile'] = request.GET.get('profile')
        return super().get(request)

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
        context['user_profile'] = self.request.session.get('user_profile')
        return context


questionnaire_list = QuestionnaireList.as_view()
questionnaire_detail = QuestionnaireDetail.as_view()
