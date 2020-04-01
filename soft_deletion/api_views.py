from django.dispatch import Signal
from django.shortcuts import get_object_or_404


from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response

from control.models import Control
from control.permissions import OnlyInspectorCanAccess


soft_delete_signal = Signal(providing_args=['obj'])


class DeleteViewSet(viewsets.ViewSet):
    permission_classes = (OnlyInspectorCanAccess,)

    def get_controls(self):
        return self.request.user.profile.controls.active()

    @decorators.action(detail=True, methods=['post'], url_path='delete-control')
    def delete_control(self, request, pk):
        control = get_object_or_404(self.get_controls(), pk=pk)
        control.delete()
        soft_delete_signal.send(
            sender=Control,
            session_user=request.user,
            obj=control)

        return Response({'status': f"Deleted {control}"})
