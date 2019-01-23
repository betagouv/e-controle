from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import EmailForm
from .models import MagicToken


class MagicLinkView(generic.FormView):
    form_class = EmailForm
    success_url = reverse_lazy('magicauth-email-sent')
    template_name = "ecc/login.html"

    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)


class ValidateTokenView(generic.RedirectView):
    url = reverse_lazy('questionnaire-list')

    def get_valid_token(self, key):
        duration = getattr(settings, 'MAGICAUTH_TOKEN_DURATION', 5 * 60)
        token = MagicToken.objects.filter(key=key).first()
        if not token:
            return None
        if token.created < timezone.now() - timedelta(seconds=duration):
            token.delete()
            return None
        return token

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        token_key = kwargs.get('key')
        token = self.get_valid_token(token_key)
        if not token:
            return redirect(settings.LOGIN_REDIRECT_URL)
        login(self.request, token.user)
        MagicToken.objects.filter(user=token.user).delete()  # Remove them all for this user
        return super().get(*args, **kwargs)


magic_link = MagicLinkView.as_view()
email_sent = generic.TemplateView.as_view(template_name='magicauth/email-sent.html')
validate_token = ValidateTokenView.as_view()
