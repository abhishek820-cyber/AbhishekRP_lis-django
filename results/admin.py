from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display  = ['order', 'assay', 'result_value', 'flag', 'entered_by', 'entered_at']
    list_filter   = ['flag']
    search_fields = ['order__order_no', 'assay__assay_code']