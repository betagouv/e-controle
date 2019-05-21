from rest_framework import viewsets

from .models import Question, Questionnaire

from .serializers import QuestionSerializer, QuestionnaireSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(
            theme__questionnaire__control__in=self.request.user.profile.controls.all())
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Instead of rendering a list, we reformat the response data to render
        a dict where the key is the question id.
        """
        response = super(QuestionViewSet, self).list(request, *args, **kwargs)
        dict_data = {}
        for elem in response.data:
            question_id = elem['id']
            dict_data[question_id] = elem
        response.data = dict_data
        return response


class QuestionnaireViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        return queryset

