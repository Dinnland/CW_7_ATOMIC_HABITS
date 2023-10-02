from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Доступ только хозяину"""
    def has_permission(self, request, view):
        if request.user == view.get_object().user:
            return True
