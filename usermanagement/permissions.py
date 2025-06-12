from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin boleh edit siapapun
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        return obj.user == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False)
