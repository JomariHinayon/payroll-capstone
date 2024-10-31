from django.contrib import admin
from .models import Account, Employee, Attendance, Payroll, Department, Position

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number', 'contact_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', )
    list_filter = ('is_active', 'is_staff')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'gender', 'birth_date', 'hire_date', 'department', 'position', 'is_active')
    list_filter = ('department', 'position', 'is_active')
    search_fields = ('id_number', 'phone_number', 'tel_number')
    ordering = ('id_number',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time_in', 'time_out', 'is_present')
    list_filter = ('date', 'is_present')
    search_fields = ('employee__id_number', 'employee__email') 

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'net_salary')
    list_filter = ('start_date', 'end_date', 'employee')
    search_fields = ('employee__id_number', 'employee__email')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'description')


admin.site.register(Account, AccountAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
