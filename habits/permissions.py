from rest_framework.permissions import BasePermission


class IsOwnerOrStaffOrModerator(BasePermission):
    """Доступ хозяину и модератору"""
    def has_permission(self, request, view):
        # manager
        if request.user.is_staff:
            return True
        elif request.user.groups.filter(name='moderator').exists():
            return True
        return request.user.is_authenticated  # owner

    def has_object_permission(self, request, view, obj):

        return request.user.groups.filter(name='moderator').exists() or request.user == obj.user


class IsNotModerator(BasePermission):
    """огран доступ модератору"""
    def has_permission(self, request, view):
        # NOT manager
        if not request.user.groups.filter(name='moderator').exists():
            return True


class ModeratorPermission(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.user.groups.filter(name='moderator').exists() or request.user.pk != view.get_object().user:
            if request.method.upper() in ['DELETE', 'POST']:
                return request.user.has_perms([
                    'habits.create_course',
                    'habits.delete_course',
                ])
        # return True
        return request.user.is_authenticated
    # def has_object_permission(self, request, view, obj):
    #     return request.user == obj.owner

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists() or request.user == obj.user


class IsOwner(BasePermission):
    """Доступ хозяину"""

    def has_permission(self, request, view):
        # owner

        if request.user == view.get_object().user:
            return True

