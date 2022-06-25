"""
Phân quyền exams_scores
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass