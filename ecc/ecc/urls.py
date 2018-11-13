from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from . import views as ecc_views

urlpatterns = [
    path('', ecc_views.home),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('admin/docs/', include('django.contrib.admindocs.urls'))]

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
