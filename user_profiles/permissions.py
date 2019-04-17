from rest_framework import permissions


class ChangeUserPermission(permissions.BasePermission):
    message = 'Add or change user is not allowed.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile.profile_type == 'inspector'
