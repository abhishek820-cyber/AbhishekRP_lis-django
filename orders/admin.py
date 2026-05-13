from django.contrib import admin
from .models import OrderTransaction, OrderLine

class OrderLineInline(admin.TabularInline):
    # Shows the assay lines directly inside the order detail page
    model  = OrderLine
    extra  = 0

@admin.register(OrderTransaction)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['order_no', 'patient', 'ordered_by', 'order_status', 'ordered_at']
    list_filter   = ['order_status']
    search_fields = ['order_no', 'patient__mrn', 'patient__patient_name']
    inlines       = [OrderLineInline]