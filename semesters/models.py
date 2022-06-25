from django.db import models

class Semesters(models.Model):
    name = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'semesters'
        
    def __str__(self):
        return str(self.name)