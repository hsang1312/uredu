from django.db import models
from teams.models import Teams
from accounts.models import Profiles

class Students(models.Model):
    team = models.OneToOneField(Teams, on_delete=models.SET_NULL, null=True)
    profile = models.OneToOneField(Profiles, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'students'
        
    def __str__(self):
        return str(self.profile.fullname)