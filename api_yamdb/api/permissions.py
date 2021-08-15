from rest_framework import permissions

class IsAdminOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == request.user.is_staff:
            return True
        return False