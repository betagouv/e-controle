import sys
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework import routers

from control import admin as admin_views
from control import api_views as control_api_views
from control import views as control_views
from demo import views as demo_views
from magicauth import views as magicauth_views
from magicauth.urls import urlpatterns as magicauth_urls
from user_profiles import api_views as user_profiles_api_views
from session import api_views as session_api_views
from tos import views as tos_views


admin.site.site_header = 'e-contrôle Administration'

router = routers.DefaultRouter()
router.register(r'annexe', control_api_views.QuestionFileViewSet, basename='annexe')
router.register(r'control', control_api_views.ControlViewSet, basename='control')
router.register(r'fichier-reponse', control_api_views.ResponseFileViewSet, basename='response-file')
router.register(r'question', control_api_views.QuestionViewSet, basename='question')
router.register(r'questionnaire', control_api_views.QuestionnaireViewSet, basename='questionnaire')
router.register(r'theme', control_api_views.ThemeViewSet, basename='theme')
router.register(r'user', user_profiles_api_views.UserProfileViewSet, basename='user')
router.register(r'session', session_api_views.SessionTimeoutViewSet, basename='session')


urlpatterns = [
    path('', magicauth_views.LoginView.as_view(), name='login'),
    path('cgu/', tos_views.tos, name='tos'),
    path(settings.ADMIN_URL_PATH, admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('bienvenue/', tos_views.Welcome.as_view(), name='welcome'),
    path('accueil/', control_views.QuestionnaireList.as_view(), name='questionnaire-list'),
    path('questionnaire/<int:pk>/', control_views.QuestionnaireDetail.as_view(), name='questionnaire-detail'),
    path('questionnaire/controle-<int:pk>/creer',
         control_views.QuestionnaireCreate.as_view(),
         name='questionnaire-create'),
    path('questionnaire/modifier/<int:pk>/',
         control_views.QuestionnaireEdit.as_view(),
         name='questionnaire-edit'),
    path('fichier-questionnaire/<int:pk>/',
         control_views.SendQuestionnaireFile.as_view(),
         name='send-questionnaire-file'),
    path('fichier-question/<int:pk>/', control_views.SendQuestionFile.as_view(), name='send-question-file'),
    path('fichier-reponse/<int:pk>/', control_views.SendResponseFile.as_view(), name='send-response-file'),

    path('upload/', control_views.UploadResponseFile.as_view(), name='response-upload'),
    path('faq/', control_views.FAQ.as_view(), name='faq'),
    path('questionnaire/corbeille/<int:pk>/', control_views.Trash.as_view(), name='trash'),

    path('megacontrole-confirmer/<int:pk>/',
         admin_views.MegacontrolConfirm.as_view(),
         name='megacontrol-confirm'),
    path('megacontrole/<int:pk>/',
         admin_views.Megacontrol.as_view(),
         name='megacontrol-done'),

    path('api/fichier-reponse/corbeille/<int:pk>/',
         control_api_views.ResponseFileTrash.as_view(),
         name='response-file-trash'),
]

urlpatterns.extend(magicauth_urls)

urlpatterns += [
    path('api/', include((router.urls, 'api'))),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    from rest_framework.documentation import include_docs_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('admin/docs/', include('django.contrib.admindocs.urls'))]
    urlpatterns += [path('api/docs/', include_docs_urls(title='e-contrôle API'))]

if settings.DEBUG and settings.ALLOW_DEMO_LOGIN:
    urlpatterns += path(
        'demo-controleur/', demo_views.DemoInspectorView.as_view(), name='demo-inspector'),
    urlpatterns += path(
        'demo/', demo_views.DemoAuditedView.as_view(), name='demo-audited'),


TESTING_MODE = 'test' in sys.argv[0]  # We want to enable the toolbar when runing tests
if settings.DEBUG or TESTING_MODE:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
