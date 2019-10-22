from django.dispatch import Signal
from rest_framework import decorators
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import UserProfile
from .permissions import ChangeUserPermission
from .serializers import UserProfileSerializer, RemoveControlSerializer


# These signals are triggered after the user is deleted via the API
user_api_post_remove = Signal(providing_args=['user_profile', 'control'])


class UserProfileViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
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
            user_api_post_remove.send(
                sender=UserProfile, session_user=self.request.user, user_profile=profile,
                control=control)
            return Response({'status': f"Removed control {control}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=False, methods=['get'])
    def current(self, request, pk=None):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)
