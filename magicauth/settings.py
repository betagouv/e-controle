from django.conf import settings as django_settings

# To add magicauth to your site, you need to add these values to your site settings (the rest have defaults, you are
# free to change them if you want):
# MAGICAUTH_FROM_EMAIL : e.g. 'contact@mysite.com'
# MAGICAUTH_LOGGED_IN_REDIRECT_URL : e.g. 'home' (this is a url name)
# MAGICAUTH_LOGIN_REDIRECT_URL : e.g. 'login' (this is a url name)

# Email settings
EMAIL_SUBJECT = getattr(django_settings, 'MAGICAUTH_EMAIL_SUBJECT', 'Lien de connexion')
EMAIL_HTML_TEMPLATE = getattr(django_settings, 'MAGICAUTH_EMAIL_HTML_TEMPLATE', 'magicauth/email.html')
EMAIL_TEXT_TEMPLATE = getattr(django_settings, 'MAGICAUTH_EMAIL_TEXT_TEMPLATE', 'magicauth/email.txt')
FROM_EMAIL = getattr(django_settings, 'MAGICAUTH_FROM_EMAIL')

# View templates
LOGIN_VIEW_TEMPLATE = getattr(django_settings, 'MAGICAUTH_LOGIN_VIEW_TEMPLATE', 'magicauth/login.html')
EMAIL_SENT_VIEW_TEMPLATE = getattr(django_settings, 'MAGICAUTH_EMAIL_SENT_VIEW_TEMPLATE', 'magicauth/email_sent.html')

# Redirects
# Once user is logged in, redirect to this url (probably your landing page).
LOGGED_IN_REDIRECT_URL = getattr(django_settings, 'MAGICAUTH_LOGGED_IN_REDIRECT_URL')
# If user is not logged in, redirect to this url to get logged in.
LOGIN_REDIRECT_URL = getattr(django_settings, 'MAGICAUTH_LOGIN_REDIRECT_URL')

# Other
TOKEN_DURATION = getattr(django_settings, 'MAGICAUTH_TOKEN_DURATION', 5 * 60)
NO_USER_CALL_BACK = getattr(django_settings, 'MAGICAUTH_NO_USER_CALL_BACK', 'magicauth.utils.raise_error')
