from django.db import models
from teams.models import Teams
from timetables.models import Shifts

class Rooms(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)
    
class Room_bookings(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
    shift = models.ForeignKey(Shifts, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)