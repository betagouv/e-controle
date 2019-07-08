from rest_framework import permissions


class ChangePermissionForInspector(permissions.BasePermission):
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
    message = 'Add or change questionnaire is not allowed.'


class ChangeControlPermission(ChangePermissionForInspector):
    message = 'Add or change control is not allowed.'
