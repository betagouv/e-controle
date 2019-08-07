from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import EmailForm
from .models import MagicToken
from . import settings as magicauth_settings


class LoginView(generic.FormView):
    """
    The login page. The user enters their email in the form to get a link by email.
    """
    form_class = EmailForm
    success_url = reverse_lazy('magicauth-email-sent')
    template_name = getattr(magicauth_settings, 'LOGIN_TEMPLATE')

    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)


class EmailSentView(generic.TemplateView):
    """
    View shown to confirm the email has been sent.
    """
    template_name = 'magicauth/email_sent.html'


class ValidateTokenView(generic.RedirectView):
    """
    The link sent by email goes to this view.
    It validates the token passed in querystring, and either logs in or shows a form to make a new token.
    """
    url = reverse_lazy('questionnaire-list')

    def get_valid_token(self, key):
        duration = getattr(magicauth_settings, 'TOKEN_DURATION')
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
            messages.warning(
                self.request,
                "Ce lien de connexion ne fonctionne plus. Pour en recevoir un nouveau, nous vous invitons à renseigner votre email ci-dessous puis à cliquer sur valider."
            )
            return redirect('login')
        login(self.request, token.user)
        MagicToken.objects.filter(user=token.user).delete()  # Remove them all for this user
        return super().get(*args, **kwargs)


