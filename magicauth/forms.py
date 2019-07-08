from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.module_loading import import_string
from ldap3 import Server, Connection, ALL, NTLM
import logging
from .models import MagicToken
import re
from django.contrib.auth.models import User
from user_profiles.models import UserProfile
from . import settings as magicauth_settings


no_user_call_back = import_string(magicauth_settings.NO_USER_CALL_BACK)


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        user_email = self.cleaned_data['email']
        user_email = user_email.lower()

        if not User.objects.filter(username__iexact=user_email).exists():
            return no_user_call_back()
            # # We now check if the user is in the active directory
            # user_info = self._check_user_in_ad(user_email)
            # if user_info:
            #     # We now create the user if it is authorized
            #     self._create_user_via_ad(user_info)
            # else:
            #     raise forms.ValidationError(_(f"Aucun utilisateur trouvé"))

        return user_email

    def _check_user_in_ad(self, user_email):
        """

        :param user_email:
        :return: Boolean
        """
        mail_regex = r'^[a-zA-Z0-9_.+-]+@(crtc\.)?ccomptes.fr$'
        if re.match(mail_regex, user_email):
            try:
                logging.info(f'Basic magicauth: LDAP Sever (username: {user_email})')
                server = Server(settings.LDAP_SERVER, get_info=ALL)
                conn = Connection(server, user=settings.LDAP_DOMAIN + "\\" + settings.LDAP_USER,
                                  password=settings.LDAP_PASSWORD, authentication=NTLM)
                logging.debug('Basic magicauth: LDAP Binding')
                if conn.bind():
                    conn.search(settings.LDAP_DC,
                                f'(&(objectClass=user)(mail={user_email}))',
                                attributes=['givenName',
                                            'company',
                                            'sn',
                                            'department',
                                            'mail'
                                            ])
                    logging.debug('Basic magicauth: LDAP search')
                    if len(conn.entries) > 0:
                        return conn.entries[0]
            except Exception as e:
                logging.error(e)
        return False

    def _create_user_via_ad(self, user_info):
        """

        :param user_info:
        """
        user = User.objects.create_user(user_info.mail.value,
                                        user_info.mail.value,
                                        '?',
                                        first_name=user_info.givenName.value,
                                        last_name=user_info.sn.value)
        UserProfile.objects.create(user=user,
                                   organization=user_info.department.value,
                                   profile_type='inspector')

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
