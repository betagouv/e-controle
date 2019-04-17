from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserProfile

from .serializers import UserProfileSerializer
from .permissions import ChangeUserPermission


class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    filterset_fields = ('controls', 'profile_type')
    permission_classes = (ChangeUserPermission,)

    def get_queryset(self):
        queryset = UserProfile.objects.filter(
            controls__in=self.request.user.profile.controls.all())
        return queryset

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        profile = self.get_object()
        profile.user.is_active = False
        profile.user.save()
        return Response({'is_active': profile.user.is_active})
