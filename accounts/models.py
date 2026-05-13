from django.db import models
from django.contrib.auth.models import User


class UserMaster(models.Model):
    """
    Extended staff profile linked to Django's built-in auth.User.
    One profile per user — stores role, employee ID, and department.
    """
    ROLE_CHOICES = [
        ("Admin",         "Admin"),
        ("Physician",     "Physician"),
        ("Nurse",         "Nurse"),
        ("Phlebotomist",  "Phlebotomist"),
        ("LabTechnician", "Lab Technician"),
    ]
    STATUS_CHOICES = [
        ("Active",   "Active"),
        ("Inactive", "Inactive"),
        ("Locked",   "Locked"),
    ]

    # One-to-one link — deleting the auth user removes the profile too
    auth_user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id  = models.CharField(max_length=20, unique=True)
    full_name    = models.CharField(max_length=150)
    role         = models.CharField(max_length=50, choices=ROLE_CHOICES)
    designation  = models.CharField(max_length=80)
    department   = models.CharField(max_length=80, blank=True, null=True)
    phone        = models.CharField(max_length=20, blank=True, null=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    class Meta:
        ordering = ["full_name"]


class UserAccessMaster(models.Model):
    """
    Defines what each role can do per module.
    Checked by middleware/permissions to gate screens and API actions.
    """
    role_name   = models.CharField(max_length=50)   # e.g. Physician
    module_name = models.CharField(max_length=80)   # e.g. patient_registration
    can_view    = models.BooleanField(default=False)
    can_create  = models.BooleanField(default=False)
    can_edit    = models.BooleanField(default=False)
    can_delete  = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role_name} → {self.module_name}"

    class Meta:
        unique_together = ("role_name", "module_name")