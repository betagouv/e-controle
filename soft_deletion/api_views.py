from django.shortcuts import get_object_or_404


from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response

from control.permissions import OnlyInspectorCanAccess


class DeleteViewSet(viewsets.ViewSet):
    permission_classes = (OnlyInspectorCanAccess,)

    def get_controls(self):
        return self.request.user.profile.controls.active()

    @decorators.action(detail=True, methods=['post'], url_path='delete-control')
    def delete_control(self, request, pk):
        control = get_object_or_404(self.get_controls(), pk=pk)
        control.delete()
        return Response({'status': f"Deleted {control}"})
