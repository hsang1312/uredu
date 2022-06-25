from django.db import models
from accounts.models import Profiles

class Teachers(models.Model):
    profile = models.OneToOneField(Profiles, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.profile.fullname)