from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import WelcomeForm


class Welcome(LoginRequiredMixin, FormView):
    template_name = "tos/welcome.html"
    form_class = WelcomeForm
    success_url = reverse_lazy('control-detail')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.user.profile.agreed_to_tos = True
        self.request.user.profile.save()
        return super().form_valid(form)


tos = TemplateView.as_view(template_name='tos/tos.html')
