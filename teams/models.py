from django.db import models
from teachers.models import Teachers
    
class Teams(models.Model):
    name = models.CharField(max_length=150, null=True)
    teacher = models.OneToOneField(Teachers, on_delete=models.SET_NULL, null=True)
    moniter = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
