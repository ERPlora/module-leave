from django.contrib import admin

from .models import LeaveType, LeaveRequest

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'days_per_year', 'is_paid', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'leave_type', 'start_date', 'end_date', 'created_at']
    search_fields = ['employee_name', 'status', 'reason']
    readonly_fields = ['created_at', 'updated_at']

