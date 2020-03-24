from django.dispatch import Signal
from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response

from control.models import Control
from control.permissions import OnlyInspectorCanAccess

soft_delete = Signal(providing_args=['obj'])


class DeleteViewSet(viewsets.ViewSet):
    permission_classes = (OnlyInspectorCanAccess,)

    def get_controls(self):
        return self.request.user.profile.controls.active()

    @decorators.action(detail=True, methods=['post'], url_path='delete-control')
    def delete_control(self, request, pk):
        control = self.get_controls().get(pk=pk)
        control.delete()
        soft_delete.send(
            sender=Control,
            obj=control)

        return Response({'status': f"Deleted {control}"})
