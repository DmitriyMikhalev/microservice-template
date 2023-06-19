from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Allow HEAD, OPTIONS for authenticated user.
    If object detail was requested (GET, POST, DELETE, PATCH, PUT) -- allowed
    only for author.
    If list of object was requested (GET) -- allows, so you have to control
    that case at view (for ex, hide other user's objects).
    """
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.author == request.user

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated
