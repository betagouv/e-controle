from actstream import action
from functools import partial
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied

from control.permissions import ChangeQuestionnairePermission
from .models import Question, Questionnaire, Theme
from .serializers import QuestionSerializer, QuestionnaireSerializer, QuestionnaireUpdateSerializer, ThemeSerializer


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
    permission_classes = (ChangeQuestionnairePermission,)

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        if not self.request.user.profile.is_inspector:
            queryset = queryset.filter(is_draft=False)
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
        self.__log_action(request.user, verb, saved_qr, saved_qr.control)

        self.__save_themes_and_questions(saved_qr=saved_qr,
                                         validated_themes_and_questions=validated_themes_and_questions,
                                         user=request.user,
                                         verb=verb)

        # Use the read serializer to output the response data.
        response.data = QuestionnaireSerializer(instance=saved_qr).data

        return response

    def create(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).create, request, *args, **kwargs)

        return self.__create_or_update(request, save_questionnaire_func, is_update=False)

    def update(self, request, *args, **kwargs):
        save_questionnaire_func = partial(super(QuestionnaireViewSet, self).update, request, *args, **kwargs)

        return self.__create_or_update(request, save_questionnaire_func, is_update=True)

    def __validate_all(self, request, pre_existing_questionnaire=None):
        serializer = QuestionnaireUpdateSerializer(pre_existing_questionnaire, data=request.data)
        serializer.is_valid(raise_exception=True)

        control = serializer.validated_data['control']
        if not request.user.profile.controls.filter(id=control.id).exists():
            e = PermissionDenied(detail='Users can only create questionnaires in controls that they belong to.',
                                 code=status.HTTP_403_FORBIDDEN)
            raise e

        return serializer.validated_data.get('themes', [])

    def __save_themes_and_questions(self, saved_qr, validated_themes_and_questions, user, verb):
        def find_child_obj_by_id(parent_obj, obj_id, obj_class):
            """
            If obj_id is in parent_obj's children, return the corresponding object. Else return none.
            :param parent_obj: e.g. an instance of Questionnaire
            :param obj_id: e.g. 3
            :param obj_class: e.g. Theme
            :return:
            """
            if parent_obj is None or obj_id is None:
                return None
            child_class_name_plural = obj_class.__name__.lower() + 's'

            children = getattr(parent_obj, child_class_name_plural)
            children_ids = children.all().values_list('id')
            if children_ids.filter(id=obj_id).exists():
                return obj_class.objects.get(id=obj_id)
            return None

        def log(saved_object):
            self.__log_action(user, verb, saved_object, saved_qr.control)

        def log_delete(saved_object):
            self.__log_action(user, 'deleted', saved_object, saved_qr.control)

        # remove themes that aren't in request.
        theme_ids_in_request = [theme_data.get('id') for theme_data in validated_themes_and_questions]
        for pre_existing_theme in saved_qr.themes.all():
            if pre_existing_theme.id not in theme_ids_in_request:
                pre_existing_theme.delete()
                log_delete(pre_existing_theme)

        # add themes that are in request
        for theme_data in validated_themes_and_questions:
            # save theme
            pre_existing_theme = find_child_obj_by_id(saved_qr, theme_data.get('id', None), Theme)
            theme_ser = ThemeSerializer(pre_existing_theme, data=theme_data)
            theme_ser.is_valid(raise_exception=True)
            saved_theme = theme_ser.save(questionnaire=saved_qr)
            log(saved_theme)

            # remove questions that aren't in request.
            questions_data = theme_data.get('questions', [])
            question_ids_in_request = [question_data.get('id') for question_data in questions_data]
            for pre_existing_question in saved_theme.questions.all():
                if pre_existing_question.id not in question_ids_in_request:
                    pre_existing_question.delete()
                    log_delete(pre_existing_question)

            # add questions that are in request
            for question_data in questions_data:
                pre_existing_question = find_child_obj_by_id(saved_theme, question_data.get('id', None), Question)
                question_ser = QuestionSerializer(pre_existing_question, data=question_data)
                question_ser.is_valid(raise_exception=True)
                saved_question = question_ser.save(theme=saved_theme)
                log(saved_question)

    def __log_action(self, user, verb, saved_object, control):
        action_details = {
            'sender': user,
            'verb': verb + ' ' + saved_object.__class__.__name__.lower(),
            'action_object': saved_object,
            'target': control,
        }
        action.send(**action_details)
