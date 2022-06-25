"""
Phân quyền semesters
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass