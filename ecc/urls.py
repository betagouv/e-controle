from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views as ecc_views
from control import views as control_views
from magicauth import views as magicauth_views


urlpatterns = [
    path('', ecc_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accueil/', control_views.questionnaire_list, name='questionnaire-list'),
    path('questionnaire/<int:pk>/', control_views.questionnaire_detail, name='questionnaire-detail'),
    path('contacts/', ecc_views.contacts, name='contacts'),
    path('suivi/', ecc_views.dashboard, name='dashboard'),
    path('login/', magicauth_views.magic_link, name='magicauth-login'),
    path('email-envoyé/', magicauth_views.email_sent, name='magicauth-email-sent'),
    path('code/<str:key>/', magicauth_views.validate_token, name='magicauth-validate-token'),
    path('upload/', control_views.upload_response_file, name='response-upload'),
    path('fichier-question/<int:pk>/', control_views.send_question_file, name='send-question-file'),
    path('fichier-reponse/<int:pk>/', control_views.send_response_file, name='send-response-file'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('admin/docs/', include('django.contrib.admindocs.urls'))]
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
