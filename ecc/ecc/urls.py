from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views as ecc_views
from control import views as control_views

urlpatterns = [
    path('', ecc_views.login, name='login'),
    path('controle/<int:control_id>/', control_views.questionnaire_list),
    path('accueil/', ecc_views.questionnaire_list, name='questionnaire-list'),
    path('questionnaire/', ecc_views.questionnaire_detail, name='questionnaire-detail'),
    path('question/', ecc_views.question_detail, name='question-detail'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [path('admin/docs/', include('django.contrib.admindocs.urls'))]
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
