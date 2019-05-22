from actstream import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import Question, Questionnaire, Theme
from .serializers import QuestionSerializer, QuestionnaireSerializer, ThemeSerializer


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


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer

    def get_queryset(self):
        queryset = Theme.objects.filter(
            questionnaire__control__in=self.request.user.profile.controls.all())
        return queryset


class QuestionnaireViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = QuestionnaireSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_id = serializer.data['control']
        if not request.user.profile.controls.filter(id=control_id).exists():
            return Response('Users can only create questionnaires in controls that they belong to.',
                            status=status.HTTP_403_FORBIDDEN)

        themes_data = request.data.pop('themes', [])

        response = super(QuestionnaireViewSet, self).create(request, *args, **kwargs)
        saved_themes = self.save_themes_and_questions(themes_data, response.data['id'])

        response.data['themes'] = saved_themes
        self.log_action(request, response)
        return response

    def log_action(self, request, response):
        control_id = int(request.data['control'])
        control = request.user.profile.controls.get(pk=control_id)
        questionnaire = control.questionnaires.get(pk=response.data['id'])
        action_details = {
            'sender': request.user,
            'verb': 'created questionnaire',
            'action_object': questionnaire,
            'target': control,
        }
        action.send(**action_details)

    def save_themes_and_questions(self, themes_data, questionnaire_id):
        saved_themes = []
        for theme_data in themes_data:
            questions_data = theme_data.pop('questions', [])
            saved_theme_json = self.save_theme(theme_data, questionnaire_id)
            saved_questions_json = self.save_questions(questions_data, saved_theme_json['id'])
            saved_theme_json['questions'] = saved_questions_json
            saved_themes.append(saved_theme_json)
        return saved_themes

    def save_theme(self, theme_data, questionnaire_id):
        theme_data['questionnaire'] = questionnaire_id
        return self.save(ThemeSerializer, 'theme', theme_data)

    def save_questions(self, questions_data, theme_id):
        saved_questions_json = []
        for question_data in questions_data:
            question_data['theme'] = theme_id
            saved_question_json = self.save(QuestionSerializer, 'question', question_data)
            saved_questions_json.append(saved_question_json)
        return saved_questions_json

    def save(self, serializer_class, data_type, data):
        serializer = serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # add the data_type to the error, otherwise it's unclear for the API client if the error is on
            # questionnaire, question or theme.
            e.detail['type'] = data_type
            raise e
        saved = serializer.save()
        saved_json = serializer.data
        return saved_json

    def update(self, request, *args, **kwargs):
        response = super(QuestionnaireViewSet, self).update(request, *args, **kwargs)
        return response
