from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
from django.utils.module_loading import import_string

from . import settings as magicauth_settings
from .models import MagicToken


email_unknown_callback = import_string(magicauth_settings.EMAIL_UNKNOWN_CALLBACK)


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        user_email = self.cleaned_data['email']
        user_email = user_email.lower()
        if not User.objects.filter(username__iexact=user_email).exists():
            email_unknown_callback(user_email)
        return user_email

    def create_token(self, user):
        token = MagicToken.objects.create(user=user)
        return token

    def send_email(self, request):
        user_email = self.cleaned_data['email']
        user = User.objects.get(username__iexact=user_email)
        token = self.create_token(user)
        email_subject = magicauth_settings.EMAIL_SUBJECT
        html_template = magicauth_settings.EMAIL_HTML_TEMPLATE
        text_template = magicauth_settings.EMAIL_TEXT_TEMPLATE
        from_email = magicauth_settings.FROM_EMAIL
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
