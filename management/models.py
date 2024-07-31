from datetime import datetime

from django.db import models
from accounts.models import User


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Project(BaseModel):
    """for storing Project details"""
    
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
        ('on hold', 'On Hold'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(BaseModel):
    """for storing Task details"""
    
    STATUS_CHOICES = (
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on hold', 'On Hold'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()   
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.assigned_to and self.assigned_to.role != "member":
            raise ValueError("Menmber can only assign task")
        super().save(*args, **kwargs)

class Milestone(BaseModel):
    """for storing Milestone details"""
    title = models.CharField(max_length=100)
    description = models.TextField()   
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    achieved_on = models.DateField(auto_now_add=True)
    
class Notification(BaseModel):
    """for storing Notification details"""
    
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
