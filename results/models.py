from django.db import models
from orders.models import OrderTransaction
from labtests.models import AssayMaster
from accounts.models import UserMaster


class Result(models.Model):
    """
    One result row per assay per order.
    Normal range and unit are snapshot-copied from AssayMaster at entry time
    so historical reports stay accurate even if master data changes later.
    """
    FLAG_CHOICES = [
        ("N",  "Normal"),
        ("H",  "High"),
        ("L",  "Low"),
        ("CR", "Critical"),
    ]

    order        = models.ForeignKey(OrderTransaction, on_delete=models.CASCADE, related_name="results")
    assay        = models.ForeignKey(AssayMaster, on_delete=models.PROTECT, related_name="results")
    result_value = models.CharField(max_length=200)
    unit         = models.CharField(max_length=40, blank=True, null=True)
    normal_range = models.CharField(max_length=100, blank=True, null=True)  # snapshot
    flag         = models.CharField(max_length=10, choices=FLAG_CHOICES, blank=True, null=True)
    remarks      = models.TextField(blank=True, null=True)

    entered_by   = models.ForeignKey(UserMaster, on_delete=models.PROTECT, related_name="results_entered")
    entered_at   = models.DateTimeField(auto_now_add=True)
    verified_by  = models.ForeignKey(UserMaster, on_delete=models.SET_NULL,
                                     related_name="results_verified", null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.order_no} / {self.assay.assay_code} = {self.result_value}"

    class Meta:
        unique_together = ("order", "assay")   # one result per test per order