"""
Phân quyền students
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass