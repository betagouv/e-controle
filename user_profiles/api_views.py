from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserProfile

from .serializers import UserProfileSerializer, RemoveControlSerializer
from .permissions import ChangeUserPermission


class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    filterset_fields = ('controls', 'profile_type')
    permission_classes = (ChangeUserPermission,)

    def get_queryset(self):
        queryset = UserProfile.objects.filter(
            controls__in=self.request.user.profile.controls.all()).distinct()
        return queryset

    @action(detail=True, methods=['post'], url_path='remove-control')
    def remove_control(self, request, pk):
        profile = self.get_object()
        serializer = RemoveControlSerializer(data=request.data)
        if serializer.is_valid():
            control = serializer.data['control']
            profile.controls.remove(control)
            return Response({'status': f"Removed control {control}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        profile = self.get_object()
        profile.user.is_active = False
        profile.user.save()
        return Response({'is_active': profile.user.is_active})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk):
        profile = self.get_object()
        profile.user.is_active = True
        profile.user.save()
        return Response({'is_active': profile.user.is_active})
