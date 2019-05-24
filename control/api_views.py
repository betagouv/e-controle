from actstream import action
from functools import partial
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

    def create_or_update(self, request, save_questionnaire_func, is_update):
        if is_update:
            pre_existing_qr = self.get_object()  # throws 404 if no qr
            verb = 'updated'
        else:
            pre_existing_qr = None
            verb = 'created'

        validated_themes_and_questions = self.validate_all(request, pre_existing_qr)
        response = save_questionnaire_func()
        saved_qr = Questionnaire.objects.get(id=response.data['id'])
        self.log_action(request.user, verb, 'questionnaire', saved_qr, saved_qr.control)

        self.save_themes_and_questions(saved_qr=saved_qr,
                                       validated_themes_and_questions=validated_themes_and_questions,
                                       user=request.user,
                                       verb=verb)
        response.data = QuestionnaireSerializer(instance=saved_qr).data

        return response

    def create(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).create, request, *args, **kwargs)

        return self.create_or_update(request, save_questionnaire_func, is_update=False)

    def update(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).update, request, *args, **kwargs)

        return self.create_or_update(request, save_questionnaire_func, is_update=True)

    def get_pre_existing_theme(self, theme_id, pre_existing_questionnaire=None):
        if pre_existing_questionnaire is None:
            return None

        # Note : Existing themes with a different parent questionnaire are ignored.
        pre_existing_theme_ids = pre_existing_questionnaire.themes.all().values_list('id')
        if pre_existing_theme_ids.filter(id=theme_id).exists():
            return Theme.objects.get(id=theme_id)
        return None

    def get_pre_existing_question(self, question_id, pre_existing_theme=None):
        if pre_existing_theme is None:
            return None

        # Note : Existing questions with a different parent are ignored.
        pre_existing_question_ids = pre_existing_theme.questions.all().values_list('id')
        if pre_existing_question_ids.filter(id=question_id).exists():
            return Question.objects.get(id=question_id)
        return None

    def validate_all(self, request, pre_existing_questionnaire=None):
        self.validate(serializer_class=QuestionnaireSerializer,
                      data_type='questionnaire',
                      data=request.data,
                      pre_existing_object=pre_existing_questionnaire)

        control_id = request.data['control']
        if not request.user.profile.controls.filter(id=control_id).exists():
            e = PermissionDenied(detail='Users can only create questionnaires in controls that they belong to.',
                                 code=status.HTTP_403_FORBIDDEN)
            raise e

        themes_data = request.data.pop('themes', [])
        validated_themes_and_questions = []
        for theme_data in themes_data:
            questions_data = theme_data.pop('questions', [])
            pre_existing_theme = self.get_pre_existing_theme(theme_data.get('id'), pre_existing_questionnaire)
            # if pre_existing_object is None, serializer.save() will create a new instance.
            validated_theme = {
                'serializer': self.validate(serializer_class=ThemeSerializer,
                                            data_type='theme',
                                            data=theme_data,
                                            pre_existing_object=pre_existing_theme),
                'questions': []
            }
            validated_themes_and_questions.append(validated_theme)
            for question_data in questions_data:
                pre_existing_question = self.get_pre_existing_question(question_data.get('id'), pre_existing_theme)
                validated_question = {
                    'serializer': self.validate(serializer_class=QuestionSerializer,
                                                data_type='question',
                                                data=question_data,
                                                pre_existing_object=pre_existing_question),
                }
                validated_theme['questions'].append(validated_question)

        return validated_themes_and_questions

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

    def save_themes_and_questions(self, saved_qr, validated_themes_and_questions, user, verb):
        def log(data_type, saved_object):
            self.log_action(user, verb, data_type, saved_object, saved_qr.control)

        log('questionnaire', saved_qr)

        for theme_to_save in validated_themes_and_questions:
            saved_theme = theme_to_save['serializer'].save(questionnaire=saved_qr)
            log('theme', saved_theme)
            for question_to_save in theme_to_save['questions']:
                saved_question = question_to_save['serializer'].save(theme=saved_theme)
                log('question', saved_question)

    def log_action(self, user, verb, data_type, saved_object, control):
        action_details = {
            'sender': user,
            'verb': verb + ' ' + data_type,
            'action_object': saved_object,
            'target': control,
        }
        action.send(**action_details)
