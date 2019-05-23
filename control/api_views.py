from actstream import action
from rest_framework import status, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

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
        qr_to_save = self.validate_all(request)

        response = super(QuestionnaireViewSet, self).create(request, *args, **kwargs)
        saved_qr = Questionnaire.objects.get(id=response.data['id'])
        self.log_action(request.user, 'questionnaire', saved_qr, saved_qr.control)

        for theme_to_save in qr_to_save['themes']:
            theme_to_save['serializer'].save(questionnaire=Questionnaire.objects.get(id=saved_qr.id))
            response.data['themes'].append(theme_to_save['serializer'].data)
            saved_theme = Theme.objects.get(id=theme_to_save['serializer'].data['id'])
            self.log_action(request.user, 'theme', saved_theme, saved_qr.control)
            for question_to_save in theme_to_save['questions']:
                question_to_save['serializer'].save(theme=Theme.objects.get(id=saved_theme.id))
                response.data['themes'][-1]['questions'].append(question_to_save['serializer'].data)
                saved_question = Theme.objects.get(id=question_to_save['serializer'].data['id'])
                self.log_action(request.user, 'question', saved_question, saved_qr.control)

        return response

    def validate_all(self, request):
        qr_to_save = {
            'serializer': self.validate(QuestionnaireSerializer, 'questionnaire', request.data),
            'themes': []
        }

        control_id = qr_to_save['serializer'].data['control']
        if not request.user.profile.controls.filter(id=control_id).exists():
            e = PermissionDenied(detail='Users can only create questionnaires in controls that they belong to.',
                                code=status.HTTP_403_FORBIDDEN)
            raise e

        themes_data = request.data.pop('themes', [])
        qr_to_save['themes'] = []
        for theme_data in themes_data:
            questions_data = theme_data.pop('questions', [])
            theme_to_save = {
                'serializer': self.validate(ThemeSerializer, 'theme', theme_data),
                'questions': []
            }
            for question_data in questions_data:
                question_to_save = {
                    'serializer': self.validate(QuestionSerializer, 'question', question_data),
                }
                theme_to_save['questions'].append(question_to_save)
            qr_to_save['themes'].append(theme_to_save)

        return qr_to_save

    def validate(self, serializer_class, data_type, data):
        serializer = serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # add the data_type to the error, otherwise it's unclear for the API client if the error is on
            # questionnaire, question or theme.
            e.detail['type'] = data_type
            raise e
        return serializer

    def log_action(self, user, data_type, saved_object, control):
        action_details = {
            'sender': user,
            'verb': 'created ' + data_type,
            'action_object': saved_object,
            'target': control,
        }
        action.send(**action_details)

    def update(self, request, *args, **kwargs):
        qr_to_save = self.validate_all(request)

        response = super(QuestionnaireViewSet, self).update(request, *args, **kwargs)
        return response
