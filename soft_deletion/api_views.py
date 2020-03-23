from rest_framework import decorators
from rest_framework import viewsets
from rest_framework.response import Response


class DeleteViewSet(viewsets.ViewSet):

    def get_controls(self):
        return self.request.user.profile.controls.active()

    @decorators.action(detail=True, methods=['post'], url_path='delete-control')
    def delete_control(self, request, pk):
        control = self.get_controls().get(pk=pk)
        control.delete()
        return Response({'status': f"Deactivated {control}"})
