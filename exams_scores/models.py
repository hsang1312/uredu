from django.db import models
from teams.models import Teams

class Exams(models.Model):
    semester = models.IntegerField()
    exam_type = models.IntegerField()
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'exams'
        
    def __str__(self):
        return str(self.id)
    
class Scores(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.SET_NULL, null=True)
    student = models.IntegerField()
    score = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'scores'
        
    def __str__(self):
        return str(self.id)