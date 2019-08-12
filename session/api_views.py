from datetime import datetime

from django.conf import settings

from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


class SessionTimeoutViewSet(viewsets.ViewSet):

    @decorators.action(detail=False, methods=['get'], url_path='expire-time')
    def expire_time(self, request):
        expire_seconds = getattr(
            settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )
        last_activity_timestamp = request.session.get(SESSION_TIMEOUT_KEY)
        expire_timestamp = last_activity_timestamp + expire_seconds
        expire_time = datetime.fromtimestamp(expire_timestamp)
        return Response({'expire': expire_time})

    @decorators.action(detail=False, methods=['get'], url_path='keep-alive')
    def keep_alive(self, request):
        return self.expire_time(request)
