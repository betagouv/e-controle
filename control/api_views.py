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

        self.save_and_build_response_data(qr_to_save, request.user, response.data, is_update=False)

        return response

    def update(self, request, *args, **kwargs):
        pre_existing_qr = self.get_object()  # throws 404 if no qr

        qr_to_save = self.validate_all(request, pre_existing_qr)

        response = super(QuestionnaireViewSet, self).update(request, *args, **kwargs)

        self.save_and_build_response_data(qr_to_save, request.user, response.data, is_update=True)

        return response

    def get_pre_existing_theme(self, theme_data, pre_existing_questionnaire=None):
        if pre_existing_questionnaire is None:
            return None

        # Note : Existing themes with a different parent questionnaire are ignored.
        pre_existing_theme_ids = pre_existing_questionnaire.themes.all().values_list('id')
        if pre_existing_theme_ids.filter(id=theme_data.get('id')).exists():
            return Theme.objects.get(id=theme_data.get('id'))
        return None

    def validate_all(self, request, pre_existing_questionnaire=None):
        qr_to_save = {
            'serializer': self.validate(serializer_class=QuestionnaireSerializer,
                                        data_type='questionnaire',
                                        data=request.data,
                                        pre_existing_object=pre_existing_questionnaire),
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
            pre_existing_theme = self.get_pre_existing_theme(theme_data, pre_existing_questionnaire)
            # if pre_existing_object is None, serializer.save() with create a new instance.
            theme_to_save = {
                'serializer': self.validate(serializer_class=ThemeSerializer,
                                            data_type='theme',
                                            data=theme_data,
                                            pre_existing_object=pre_existing_theme),
                'questions': []
            }
            for question_data in questions_data:
                question_to_save = {
                    'serializer': self.validate(QuestionSerializer, 'question', question_data),
                }
                theme_to_save['questions'].append(question_to_save)
            qr_to_save['themes'].append(theme_to_save)

        return qr_to_save

    def validate(self, serializer_class, data_type, data, pre_existing_object=None):
        if pre_existing_object is None:
            serializer = serializer_class(data=data)
        else:
            serializer = serializer_class(pre_existing_object, data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # add the data_type to the error, otherwise it's unclear for the API client if the error is on
            # questionnaire, question or theme.
            e.detail['type'] = data_type
            raise e
        return serializer

    def save_and_build_response_data(self, qr_to_save, user, response_data, is_update=False):
        verb = 'updated' if is_update else 'created'
        saved_qr = Questionnaire.objects.get(id=response_data['id'])

        def log(data_type, saved_object):
            action_details = {
                'sender': user,
                'verb': verb + ' ' + data_type,
                'action_object': saved_object,
                'target': saved_qr.control,
            }
            action.send(**action_details)

        log('questionnaire', saved_qr)

        for theme_to_save in qr_to_save['themes']:
            theme_to_save['serializer'].save(questionnaire=Questionnaire.objects.get(id=saved_qr.id))
            response_data['themes'].append(theme_to_save['serializer'].data)
            saved_theme = Theme.objects.get(id=theme_to_save['serializer'].data['id'])
            log('theme', saved_theme)
            for question_to_save in theme_to_save['questions']:
                question_to_save['serializer'].save(theme=Theme.objects.get(id=saved_theme.id))
                response_data['themes'][-1]['questions'].append(question_to_save['serializer'].data)
                saved_question = Theme.objects.get(id=question_to_save['serializer'].data['id'])
                log('question', saved_question)
