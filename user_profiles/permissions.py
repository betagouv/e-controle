from rest_framework import permissions


class CreateUserPermission(permissions.BasePermission):
    message = 'Creating user is not allowed.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile.profile_type == 'inspector'
