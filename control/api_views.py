from actstream import action
from functools import partial
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Question, Questionnaire, Theme
from .serializers import QuestionSerializer, QuestionnaireSerializer, QuestionnaireWriteSerializer, ThemeSerializer


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

    def __create_or_update(self, request, save_questionnaire_func, is_update):
        if is_update:
            pre_existing_qr = self.get_object()  # throws 404 if no qr
            verb = 'updated'
        else:
            pre_existing_qr = None
            verb = 'created'

        validated_themes_and_questions = self.__validate_all(request, pre_existing_qr)
        response = save_questionnaire_func()
        saved_qr = Questionnaire.objects.get(id=response.data['id'])
        self.__log_action(request.user, verb, 'questionnaire', saved_qr, saved_qr.control)

        self.__save_themes_and_questions(saved_qr=saved_qr,
                                         validated_themes_and_questions=validated_themes_and_questions,
                                         user=request.user,
                                         verb=verb)
        response.data = QuestionnaireSerializer(instance=saved_qr).data

        return response

    def create(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).create, request, *args, **kwargs)

        return self.__create_or_update(request, save_questionnaire_func, is_update=False)

    def update(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).update, request, *args, **kwargs)

        return self.__create_or_update(request, save_questionnaire_func, is_update=True)

    def __validate_all(self, request, pre_existing_questionnaire=None):
        def validate(serializer_class, data_type, data, pre_existing_object=None):
            if pre_existing_object is None:
                serializer = serializer_class(data=data)
            else:
                serializer = serializer_class(pre_existing_object, data=data)

            serializer.is_valid(raise_exception=True)
            return serializer

        def get_pre_existing_child(child_id, child_class, pre_existing_parent=None):
            if pre_existing_parent is None:
                return None
            child_class_name_plural = child_class.__name__.lower() + 's'

            # Note : Existing children with a different parent are ignored.
            children = getattr(pre_existing_parent, child_class_name_plural)
            pre_existing_child_ids = children.all().values_list('id')
            if pre_existing_child_ids.filter(id=child_id).exists():
                return child_class.objects.get(id=child_id)
            return None

        def validate_child(child_data, child_class, child_serializer_class, pre_existing_parent):
            child_class_name = child_class.__name__.lower()
            pre_existing_child = get_pre_existing_child(child_data.get('id'), child_class, pre_existing_parent)
            # if pre_existing_object is None, serializer.save() will create a new instance.
            serializer = validate(serializer_class=child_serializer_class,
                                  data_type=child_class_name,
                                  data=child_data,
                                  pre_existing_object=pre_existing_child)
            return serializer, pre_existing_child

        serializer = validate(serializer_class=QuestionnaireWriteSerializer,
                 data_type='questionnaire',
                 data=request.data,
                 pre_existing_object=pre_existing_questionnaire)

        control = serializer.validated_data['control']
        if not request.user.profile.controls.filter(id=control.id).exists():
            e = PermissionDenied(detail='Users can only create questionnaires in controls that they belong to.',
                                 code=status.HTTP_403_FORBIDDEN)
            raise e

        themes_data = request.data.pop('themes', [])
        validated_themes_and_questions = []
        for theme_data in themes_data:
            questions_data = theme_data.pop('questions', [])
            (serializer, pre_existing_theme) = \
                validate_child(theme_data, Theme, ThemeSerializer, pre_existing_questionnaire)
            validated_themes_and_questions.append({
                'serializer': serializer,
                'questions': []
            })
            for question_data in questions_data:
                (serializer, _) = validate_child(question_data, Question, QuestionSerializer, pre_existing_theme)
                validated_themes_and_questions[-1]['questions'].append({
                    'serializer': serializer
                })

        return validated_themes_and_questions

    def __save_themes_and_questions(self, saved_qr, validated_themes_and_questions, user, verb):
        def log(data_type, saved_object):
            self.__log_action(user, verb, data_type, saved_object, saved_qr.control)

        log('questionnaire', saved_qr)

        for theme_to_save in validated_themes_and_questions:
            saved_theme = theme_to_save['serializer'].save(questionnaire=saved_qr)
            log('theme', saved_theme)
            for question_to_save in theme_to_save['questions']:
                saved_question = question_to_save['serializer'].save(theme=saved_theme)
                log('question', saved_question)

    def __log_action(self, user, verb, data_type, saved_object, control):
        action_details = {
            'sender': user,
            'verb': verb + ' ' + data_type,
            'action_object': saved_object,
            'target': control,
        }
        action.send(**action_details)
