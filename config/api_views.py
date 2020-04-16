from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response


class ConfigViewSet(viewsets.ViewSet):

    def list(self, request):
        config = {
            'support_team_email': settings.SUPPORT_TEAM_EMAIL,
            'static_files_url': settings.STATIC_URL
        }
        if request.user.profile.is_inspector:
            config.update({
                'webdav_url': settings.WEBDAV_URL,
            })
        return Response(config)
