from django.conf import settings


NO_USER_CALL_BACK = getattr(settings, 'MAGICAUTH_NO_USER_CALL_BACK', 'magicauth.utils.raise_error')
EMAIL_SUBJECT = getattr(settings, 'MAGICAUTH_EMAIL_SUBJECT', 'Connexion e-controle')
EMAIL_SUBJECT = getattr(settings, 'MAGICAUTH_EMAIL_HTML_TEMPLATE', 'magicauth/email.html')
EMAIL_TEXT_TEMPLATE = getattr(settings, 'MAGICAUTH_EMAIL_TEXT_TEMPLATE', 'magicauth/email.txt')
FROM_EMAIL = getattr(settings, 'MAGICAUTH_FROM_EMAIL')
