from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from .models import MagicToken

User = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if not User.objects.filter(email=user_email).exists():
            raise forms.ValidationError(_(f"Aucun utilisateur trouvé"))
        return user_email

    def create_token(self, user):
        token = MagicToken.objects.create(user=user)
        return token

    def send_email(self, request):
        user_email = self.cleaned_data['email']
        user = User.objects.get(email=user_email)
        token = self.create_token(user)
        email_subject = getattr(settings, 'MAGICAUTH_EMAIL_SUBJECT', 'Connection e-controle')
        html_template = getattr(settings, 'MAGICAUTH_EMAIL_HTML_TEMPLATE', 'magicauth/email.html')
        text_template = getattr(settings, 'MAGICAUTH_EMAIL_TEXT_TEMPLATE', 'magicauth/email.txt')
        from_email = getattr(settings, 'MAGICAUTH_FROM_EMAIL', 'econtrole@bate.ccomptes.fr')
        context = {
            'token': token,
            'user': user,
            'site': request.site,
        }
        text_message = loader.render_to_string(text_template, context)
        html_message = loader.render_to_string(html_template, context)
        send_mail(
            subject=email_subject,
            message=text_message,
            from_email=from_email,
            html_message=html_message,
            recipient_list=[user_email],
            fail_silently=False,
        )
