import sys
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework import routers

from . import views as ecc_views
from control import views as control_views
from control import api_views as control_api_views
from magicauth import views as magicauth_views


admin.site.site_header = 'e-contrôle Administration'

router = routers.DefaultRouter()
router.register(r'question', control_api_views.QuestionViewSet, basename='question')


urlpatterns = [
    path('', ecc_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accueil/', control_views.questionnaire_list, name='questionnaire-list'),
    path('questionnaire/<int:pk>/', control_views.questionnaire_detail, name='questionnaire-detail'),
    path('login/', magicauth_views.magic_link, name='magicauth-login'),
    path('email-envoyé/', magicauth_views.email_sent, name='magicauth-email-sent'),
    path('code/<str:key>/', magicauth_views.validate_token, name='magicauth-validate-token'),
    path('upload/', control_views.upload_response_file, name='response-upload'),
    path('fichier-questionnaire/<int:pk>/', control_views.send_questionnaire_file, name='send-questionnaire-file'),
    path('fichier-question/<int:pk>/', control_views.send_question_file, name='send-question-file'),
    path('fichier-reponse/<int:pk>/', control_views.send_response_file, name='send-response-file'),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/', include((router.urls, 'api'))),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    from rest_framework.documentation import include_docs_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('admin/docs/', include('django.contrib.admindocs.urls'))]
    urlpatterns += [path('api/docs/', include_docs_urls(title='e-contrôle API'))]


TESTING_MODE = 'test' in sys.argv[0]  # We want to enable the toolbar when runing tests
if settings.DEBUG or TESTING_MODE:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
