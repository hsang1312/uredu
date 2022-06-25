"""
Phân quyền teams
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass