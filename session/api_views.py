from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response


class SessionTimeoutViewSet(viewsets.ViewSet):

    @decorators.action(detail=False, methods=['get'], url_path='keep-alive')
    def keep_alive(self, request):
        return Response({})
