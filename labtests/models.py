from django.db import models


class TestMenuMaster(models.Model):
    """
    Groups assays by lab department/panel.
    e.g. Serology Panel (SERO), Haematology (HAEM).
    """
    DEPARTMENT_CHOICES = [
        ("Serology",      "Serology"),
        ("Haematology",   "Haematology"),
        ("Biochemistry",  "Biochemistry"),
        ("Microbiology",  "Microbiology"),
        ("Immunology",    "Immunology"),
        ("Other",         "Other"),
    ]
    STATUS_CHOICES = [("Active", "Active"), ("Inactive", "Inactive")]

    menu_code   = models.CharField(max_length=20, unique=True)   # e.g. SERO
    menu_name   = models.CharField(max_length=100)
    department  = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    description = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.menu_code} — {self.menu_name}"

    class Meta:
        ordering = ["menu_code"]


class AssayMaster(models.Model):
    """
    An individual lab test linked to a TestMenu.
    Normal range and unit are stored here and snapshot-copied to Result on entry.
    """
    STATUS_CHOICES = [("Active", "Active"), ("Inactive", "Inactive")]

    menu         = models.ForeignKey(TestMenuMaster, on_delete=models.PROTECT, related_name="assays")
    assay_code   = models.CharField(max_length=20, unique=True)   # e.g. CBC, FBS
    assay_name   = models.CharField(max_length=150)
    sample_type  = models.CharField(max_length=50)                # Blood / Urine / Swab
    tat_hours    = models.PositiveSmallIntegerField(blank=True, null=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    normal_range = models.CharField(max_length=100, blank=True, null=True)
    unit         = models.CharField(max_length=40, blank=True, null=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assay_code} — {self.assay_name}"

    class Meta:
        ordering = ["assay_code"]