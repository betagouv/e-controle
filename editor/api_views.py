from rest_framework import generics

from control.models import Questionnaire
from .serializers import UpdateEditorSerializer


class UpdateEditor(generics.UpdateAPIView):
    serializer_class = UpdateEditorSerializer

    def get_queryset(self):
        if not self.request.user.profile.is_inspector:
            return Questionnaire.objects.none()

        queryset = Questionnaire.objects  \
            .filter(control__in=self.request.user.profile.controls.all())  \
            .filter(is_draft=True)
        return queryset
