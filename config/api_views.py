from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response


class ConfigViewSet(viewsets.ViewSet):

    def list(self, request):
        config = {'support_team_email': settings.SUPPORT_TEAM_EMAIL}
        return Response(config)
