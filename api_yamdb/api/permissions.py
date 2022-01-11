from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_moderator
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_moderator
            or request.user.is_staff
        )


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
        )


class IsAllReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
