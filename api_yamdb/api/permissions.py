from rest_framework import permissions


#  Для произведений, жанров и категорий
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


# Для отзывов и комментов?
class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    #  user может читать всё, дополнительно он может
    #  публиковать отзывы и ставить оценку произведениям,
    #  может комментировать чужие отзывы; может редактировать и удалять
    # свои отзывы и комментарии.
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method is permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
