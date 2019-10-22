from actstream import action
from rest_framework import decorators
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import UserProfile
from .permissions import ChangeUserPermission
from .serializers import UserProfileSerializer, RemoveControlSerializer


class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    filterset_fields = ('controls', 'profile_type')
    search_fields = ('=user__username',)
    permission_classes = (ChangeUserPermission,)

    def get_queryset(self):
        queryset = UserProfile.objects.filter(
            controls__in=self.request.user.profile.controls.all()).distinct()
        return queryset

    @decorators.action(detail=True, methods=['post'], url_path='remove-control')
    def remove_control(self, request, pk):
        profile = self.get_object()
        serializer = RemoveControlSerializer(data=request.data)
        if serializer.is_valid():
            control_id = serializer.data['control']
            control = profile.controls.get(pk=control_id)
            profile.controls.remove(control)
            if profile.is_inspector:
                verb = 'removed inspector user'
            if profile.is_audited:
                verb = 'removed audited user'
            action_details = {
                'sender': self.request.user,
                'verb': verb,
                'action_object': profile,
                'target': control,
            }
            action.send(**action_details)
            return Response({'status': f"Removed control {control}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=False, methods=['get'])
    def current(self, request, pk=None):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)
