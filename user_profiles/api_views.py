from rest_framework import viewsets, mixins

from .models import UserProfile

from .serializers import UserProfileSerializer
from .permissions import CreateUserPermission

class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    filterset_fields = ('controls', 'profile_type')
    permission_classes = (CreateUserPermission,)

    def get_queryset(self):
        queryset = UserProfile.objects.filter(
            controls__in=self.request.user.profile.controls.all())
        return queryset
