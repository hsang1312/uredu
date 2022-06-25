from django.db import models

class Subjects(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    head_teacher = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)