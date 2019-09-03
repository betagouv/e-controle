from django.conf import settings

from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


class SessionTimeoutViewSet(viewsets.ViewSet):

    @decorators.action(detail=False, methods=['get'], url_path='get-timeout')
    def get_timeout(self, request):
        expire_seconds = getattr(
            settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )
        return Response({
            'backend_expire': expire_seconds,
            'frontend_expire': round(expire_seconds - expire_seconds*0.1),
        })

    @decorators.action(detail=False, methods=['get'], url_path='keep-alive')
    def keep_alive(self, request):
        return self.get_timeout(request)
