"""
Phân quyền rooms
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass