from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta


from .models import Account, Employee, Attendance, Payroll, Department, Position, Announcement


class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number', 'contact_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', )
    list_filter = ('is_active', 'is_staff')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'user', 'gender', 'birth_date', 'hire_date', 'department', 'position', 'is_active', 'display_image', 'display_fingerprint', 'calculate_salary_button')
    list_filter = ('department', 'position', 'is_active')
    search_fields = ('id_number', 'phone_number', 'tel_number')
    ordering = ('id_number',)

    def display_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.profile_image.url)
        return "No Image"

    display_image.short_description = "Profile Image"

    def display_fingerprint(self, obj):
        if obj.fingerprint_file and obj.fingerprint_file.name.endswith('.dat'):
            return format_html('<a href="{}" download>Download Fingerprint</a>', obj.fingerprint_file.url)
        return "No Fingerprint File"

    display_fingerprint.short_description = "Fingerprint File"

    readonly_fields = ('display_image', 'display_fingerprint')

    # Add a custom button to calculate salary
    def calculate_salary_button(self, obj):
        return format_html(
            '<a class="button" href="/calculate_salary/{}/">Calculate Salary</a>', obj.id
        )

    calculate_salary_button.short_description = "Salary Action"

    # Register the action in the admin interface
    actions = ['calculate_salary']

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

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image_preview')
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.announcement_image:
            return format_html('<img src="{}" style="height: 75px;"/>', obj.announcement_image.url)
        return "No Image"

    image_preview.short_description = 'Preview'


admin.site.register(Account, AccountAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
