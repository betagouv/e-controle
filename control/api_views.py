from rest_framework import viewsets

from .models import Question, Comment

from .serializers import QuestionSerializer, CommentSerializer

from rest_framework.renderers import JSONRenderer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(
            theme__questionnaire__control=self.request.user.profile.control)
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

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        """
        If one of the query params is question_id we restrict queryset which belong to this id
        """
        queryset = Comment.objects.all()
        question_id = self.request.query_params.get('questionid', None)

        queryset = queryset.filter(
            question__theme__questionnaire__control=self.request.user.profile.control)

        if question_id is not None:
            queryset = queryset.filter(question__id = question_id)

        return queryset
