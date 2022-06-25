from django.db import models
from teams.models import Teams
from teachers.models import Teachers
from subjects.models import Subjects
from semesters.models import Semesters

class Timetables(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semesters, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
class Timetable_details(models.Model):
    timetable = models.OneToOneField(Timetables, on_delete=models.SET_NULL, null=True)
    teacher = models.OneToOneField(Teachers, on_delete=models.SET_NULL, null=True)
    shift = models.OneToOneField('Shifts', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.timetable)

class Timetable_requirements(models.Model):
    subject = models.IntegerField(null=True)
    block = models.IntegerField(null=True)
    day_maximum = models.IntegerField(null=True)
    week_maximum = models.IntegerField(null=True)
    timetable = models.OneToOneField(Timetables, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
class Block_requirements(models.Model):
    required = models.ForeignKey(Timetable_requirements, on_delete=models.SET_NULL, null=True)
    block_number = models.IntegerField(null=True)
    day_number = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
class Shifts(models.Model):
    date_index = models.IntegerField(null=True)
    start = models.CharField(max_length=150, null=True)
    end = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.date_index)
    
    
class Attendances(models.Model):
    timetable_detail_id = models.IntegerField(null=True)
    student_id = models.IntegerField(null=True)
    is_attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student_id)
    


