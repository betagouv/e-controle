from django.urls import reverse_lazy
from django.views import generic

from .forms import EmailForm


class MagicLinkView(generic.FormView):
    form_class = EmailForm
    success_url = reverse_lazy('magicauth-email-sent')
    template_name = "ecc/login.html"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


magic_link = MagicLinkView.as_view()
email_sent = generic.TemplateView.as_view(template_name='magicauth/email-sent.html')
