"""
Phân quyền accounts
"""
from rest_framework import permissions
from constants import roles
from accounts import models

def role_permissions(request):
    try:
        role_per = request.user.role
    except AttributeError:
        return False
    return True

class IsAdmin(permissions.BasePermission):
    """
    Is exactly admin
    """
    def has_permission(self, request, view):
        if role_permissions(request):
            return bool(request.user and request.user.role == roles.ADMIN)
        return False
    
    def has_object_permission(self, request, view, object):
        if role_permissions(request):
            return bool(request.user and request.user.role == roles.ADMIN)
        return False