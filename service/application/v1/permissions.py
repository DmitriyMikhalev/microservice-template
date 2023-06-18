from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Allow HEAD, OPTIONS for authenticated user.
    If object detail was requested (GET, POST, DELETE, PATCH, PUT) -- allowed
    If list of object was requested (GET) -- allows, so you have to control
    that case at view.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated
