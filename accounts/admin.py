from django.contrib import admin
from .models import UserMaster, UserAccessMaster

@admin.register(UserMaster)
class UserMasterAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'role', 'employee_id', 'department', 'status']
    list_filter   = ['role', 'status']
    search_fields = ['full_name', 'employee_id']

@admin.register(UserAccessMaster)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'module_name', 'can_view', 'can_create', 'can_edit', 'can_delete']
    list_filter  = ['role_name']