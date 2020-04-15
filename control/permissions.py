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


class OnlyEditorCanChangeQuestionnaire(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        questionnaire = obj
        if not questionnaire.editor:
            return False
        if questionnaire.editor == request.user:
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
