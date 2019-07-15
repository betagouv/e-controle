from rest_framework import permissions


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


class ChangeControlPermission(ChangePermissionForInspector):
    message = ChangePermissionForInspector.message_format.format('control')
