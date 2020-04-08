from rest_framework import permissions
from rest_framework.exceptions import ParseError

from control.models import Questionnaire


class OnlyInspectorCanAccess(permissions.BasePermission):
    message_format = 'Accessing this resource is not allowed.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.profile.is_inspector


class OnlyInspectorCanChange(permissions.BasePermission):
    message_format = 'Adding or changing this resource is not allowed.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile.is_inspector


class ChangeQuestionnairePermission(OnlyInspectorCanChange):

    def has_permission(self, request, view):
        if not super(ChangeQuestionnairePermission, self).has_permission(request, view):
            return False
        if request.parser_context.get('kwargs') is None or request.parser_context['kwargs'].get('pk') is None:
            return True
        questionnaire_id = request.parser_context['kwargs']['pk']
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        if not questionnaire.editor:
            return False
        if not questionnaire.is_draft:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if questionnaire.editor.pk == request.user.pk:
            return True
        return False


class ControlIsNotDeleted(permissions.BasePermission):
    message_format = 'Accessing this resource is not allowed.'

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'control'):
            raise ParseError(detail='Missing attribute "control" during permission check')
        return not obj.control.is_deleted()


class QuestionnaireIsDraft(permissions.BasePermission):
    message_format = 'Accessing this resource is not allowed.'

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'questionnaire'):
            raise ParseError(detail='Missing attribute "questionnaire" during permission check')
        return obj.questionnaire.is_draft
