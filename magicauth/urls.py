from django.urls import path

from . import views as magicauth_views
from . import settings as magicauth_settings

urlpatterns = [
    path(magicauth_settings.LOGIN_URL, magicauth_views.LoginView.as_view(), name='magicauth-login'),
    path(magicauth_settings.EMAIL_SENT_URL, magicauth_views.EmailSentView.as_view(), name='magicauth-email-sent'),
    path('code/<str:key>/', magicauth_views.ValidateTokenView.as_view(), name=magicauth_settings.VALIDATE_TOKEN_URL),
]
