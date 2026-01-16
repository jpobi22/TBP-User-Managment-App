from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    metadata = models.JSONField(default=dict, blank=True)

    department = models.CharField(max_length=120, blank=True)  
    job_title = models.CharField(max_length=120, blank=True)  
    is_active_employee = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
