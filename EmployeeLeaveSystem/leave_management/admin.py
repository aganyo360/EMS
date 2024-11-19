from django.contrib import admin
from .models import Department, Employee, LeaveType, Leave, AdminProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'creation_date')
    search_fields = ('name', 'short_name', 'code')
    list_filter = ('creation_date',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'first_name', 'last_name', 'department', 'status', 'reg_date')
    search_fields = ('emp_id', 'first_name', 'last_name', 'phone_number')
    list_filter = ('department', 'status', 'reg_date')
    ordering = ('reg_date',)


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_date')
    search_fields = ('name',)
    list_filter = ('creation_date',)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'from_date', 'to_date', 'status', 'posting_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type__name')
    list_filter = ('status', 'leave_type', 'posting_date')
    ordering = ('-posting_date',)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'updation_date')
    search_fields = ('fullname', 'email')
    list_filter = ('updation_date',)
