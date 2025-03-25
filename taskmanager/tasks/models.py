from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assign tasks to users
    title = models.CharField(max_length=200)  # Task name
    description = models.TextField(blank=True)  # Optional details
    start_date = models.DateField(null=True, blank=True)  # New field
    end_date = models.DateField(null=True, blank=True)  # New field
    completed = models.BooleanField(default=False)  # Task status
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.title  # Display task title in admin panel
    


class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)  # Allow null values

    def __str__(self):
        return f"{self.admin} - {self.action} on Task {self.task.id if self.task else 'N/A'}"
