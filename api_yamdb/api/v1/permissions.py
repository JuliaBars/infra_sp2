from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать
    объект только админу.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdmin(BasePermission):
    """
    Доступ только администаторам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать
    объект только админу, модератору или автору.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
            or request.user.is_superuser
        )
