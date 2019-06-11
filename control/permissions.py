from rest_framework import permissions


class ChangeQuestionnairePermission(permissions.BasePermission):
    message = 'Add or change questionnaire is not allowed.'

    def has_permission(self, request, view):
        try:
            if request.user.profile.is_inspector:
                return True
        except AttributeError:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        return False
