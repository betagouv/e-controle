from django.urls import path

from . import views as magicauth_views
from . import settings as magicauth_settings

urlpatterns = [
    path('login/', magicauth_views.LoginView.as_view(), name=magicauth_settings.LOGIN_URL),
    path('email-envoyé/', magicauth_views.EmailSentView.as_view(), name=magicauth_settings.EMAIL_SENT_REDIRECT_URL),
    path('code/<str:key>/', magicauth_views.ValidateTokenView.as_view(), name=magicauth_settings.VALIDATE_TOKEN_URL),
]
