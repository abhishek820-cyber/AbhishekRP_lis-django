from django.contrib import admin
from .models import PatientMaster

@admin.register(PatientMaster)
class PatientAdmin(admin.ModelAdmin):
    list_display  = ['mrn', 'patient_name', 'age', 'gender', 'nationality', 'status']
    list_filter   = ['gender', 'status']
    search_fields = ['mrn', 'patient_name', 'phone']