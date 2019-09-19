from rest_framework import permissions
from control.models import Questionnaire

class ChangePermissionForInspector(permissions.BasePermission):
    message_format = 'Adding or changing {} is not allowed.'

    def has_permission(self, request, view):
        try:
            if request.user.profile.is_inspector:
                return True
        except AttributeError:
            # user not logged in
            return False

        # logged in user, not inspector
        if request.method in permissions.SAFE_METHODS:
            # can read
            return True
        # cannot write
        return False


class ChangeQuestionnairePermission(ChangePermissionForInspector):
    message = ChangePermissionForInspector.message_format.format('questionnaire')

    def has_permission(self, request, view):
        if not super(ChangeQuestionnairePermission, self).has_permission(request, view):
            return False

        if request.parser_context.get('kwargs') is None or request.parser_context['kwargs'].get('pk') is None:
            return True

        questionnaire_id = request.parser_context['kwargs']['pk']
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)

        if not questionnaire.is_draft:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if questionnaire.author_id is None:
            return True

        if questionnaire.author_id == request.user.id:
            return True
        return False


class ChangeControlPermission(ChangePermissionForInspector):
    message = ChangePermissionForInspector.message_format.format('control')
