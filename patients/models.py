from django.db import models


class PatientMaster(models.Model):
    """
    Core demographic record for every patient.
    MRN is the unique patient identifier used across all modules.
    Auto-generated as PAT-000001 or entered manually.
    """
    GENDER_CHOICES = [
        ("Male",   "Male"),
        ("Female", "Female"),
        ("Other",  "Other"),
    ]
    STATUS_CHOICES = [
        ("Active",   "Active"),
        ("Inactive", "Inactive"),
    ]

    mrn          = models.CharField(max_length=20, unique=True)      # e.g. PAT-000001
    patient_name = models.CharField(max_length=150)
    age          = models.PositiveSmallIntegerField()                # 0–150
    gender       = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality  = models.CharField(max_length=80)
    dob          = models.DateField(blank=True, null=True)           # optional; used to auto-calc age
    phone        = models.CharField(max_length=20, blank=True, null=True)
    email        = models.EmailField(max_length=150, blank=True, null=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mrn} — {self.patient_name}"

    class Meta:
        ordering = ["-created_at"]