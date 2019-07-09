from ldap3 import Server, Connection, ALL, NTLM
import logging
import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from user_profiles.models import UserProfile


def active_directory_auth(user_email=None):
    # We now check if the user is in the active directory
    user_info = get_user_form_ad(user_email)
    if user_info:
        # We now create the user if it is authorized
        create_user(user_info)
    else:
        raise forms.ValidationError(f"Aucun utilisateur trouvé")


def get_user_form_ad(user_email):
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


def create_user(self, user_info):
    """

    :param user_info:
    """
    user = User.objects.create_user(user_info.mail.value,
                                    user_info.mail.value,
                                    '?',
                                    first_name=user_info.givenName.value,
                                    last_name=user_info.sn.value)
    UserProfile.objects.create(user=user,
                               organization=user_info.company.value,
                               profile_type='inspector')
