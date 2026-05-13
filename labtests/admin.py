from django.contrib import admin
from .models import TestMenuMaster, AssayMaster

@admin.register(TestMenuMaster)
class TestMenuAdmin(admin.ModelAdmin):
    list_display  = ['menu_code', 'menu_name', 'department', 'status']
    list_filter   = ['department', 'status']
    search_fields = ['menu_code', 'menu_name']

@admin.register(AssayMaster)
class AssayAdmin(admin.ModelAdmin):
    list_display  = ['assay_code', 'assay_name', 'menu', 'sample_type', 'price', 'status']
    list_filter   = ['status', 'menu']
    search_fields = ['assay_code', 'assay_name']