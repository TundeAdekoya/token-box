from rest_framework import permissions

class isAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

def has_permission(self, request, view, obj=None):
    # Write permissions are only allowed to the owner of the snippet
    return obj is None or obj.from_user == request.user