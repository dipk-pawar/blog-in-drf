from rest_framework.permissions import BasePermission


class SuperuserOnly(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a superuser
        return (
            request.user
            and request.user.is_active
            and request.user.is_authenticated
            and request.user.is_superadmin
        )


class SuperuserORLoggedinUser(BasePermission):
    def has_permission(self, request, view):
        # Allow all authenticated users

        return request.user and request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        # Allow superusers or the user itself to access the object (user)
        return request.user.is_active and (
            request.user.is_superadmin or obj == request.user
        )
