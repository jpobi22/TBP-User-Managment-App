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

    class Meta:
        permissions = [
            ("access_it_portal", "Can access IT portal"),
            ("access_hr_portal", "Can access HR portal"),
            ("access_sales_portal", "Can access Sales portal"),
            ("access_audit_portal", "Can access Audit portal"),
        ]

    def __str__(self):
        return f"Profile: {self.user.username}"


class AuditLog(models.Model):
    occurred_at = models.DateTimeField()
    table_name = models.TextField()
    action = models.TextField()
    row_pk = models.TextField(null=True, blank=True)
    changed_by = models.TextField(null=True, blank=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "audit_log"
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"{self.occurred_at} {self.table_name} {self.action}"
