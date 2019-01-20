from rest_framework import viewsets

from .models import Question

from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(theme__questionnaire__control=self.request.user.profile.control)
        return queryset
