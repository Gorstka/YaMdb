from rest_framework import permissions


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_authenticated):
            return (request.user.role == "admin"
                    or request.user.is_staff
                    or request.user.is_superuser
                    )
        return False
