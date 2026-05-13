from django.db import models
from patients.models import PatientMaster
from accounts.models import UserMaster
from labtests.models import AssayMaster


class OrderTransaction(models.Model):
    """
    Header record for a lab order session.
    Status moves linearly: Ordered→Collected→In-Lab→Completed.
    Only the designated role may advance each step (enforced in views).
    """
    STATUS_ORDERED   = 1
    STATUS_COLLECTED = 2
    STATUS_IN_LAB    = 3
    STATUS_COMPLETED = 4

    STATUS_CHOICES = [
        (STATUS_ORDERED,   "Ordered"),
        (STATUS_COLLECTED, "Collected"),
        (STATUS_IN_LAB,    "In-Lab"),
        (STATUS_COMPLETED, "Completed"),
    ]

    order_no     = models.CharField(max_length=20, unique=True)  # e.g. ORD-20260001
    patient      = models.ForeignKey(PatientMaster, on_delete=models.PROTECT, related_name="orders")
    ordered_by   = models.ForeignKey(UserMaster, on_delete=models.PROTECT, related_name="orders_placed")
    ordered_at   = models.DateTimeField(auto_now_add=True)

    # Filled by Phlebotomist on sample collection
    collected_by = models.ForeignKey(UserMaster, on_delete=models.SET_NULL,
                                     related_name="orders_collected", null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    # Filled by Lab Technician on sample receipt in lab
    received_by  = models.ForeignKey(UserMaster, on_delete=models.SET_NULL,
                                     related_name="orders_received", null=True, blank=True)
    received_at  = models.DateTimeField(null=True, blank=True)

    order_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ORDERED)
    notes        = models.TextField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_no} ({self.get_order_status_display()})"

    class Meta:
        ordering = ["-ordered_at"]


class OrderLine(models.Model):
    """
    One assay (test) within an order.
    An order can have many lines; each line is one test.
    """
    order      = models.ForeignKey(OrderTransaction, on_delete=models.CASCADE, related_name="lines")
    assay      = models.ForeignKey(AssayMaster, on_delete=models.PROTECT, related_name="order_lines")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("order", "assay")   # no duplicate test in same order