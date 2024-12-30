from django.db import models
from datetime import time
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from config import settings
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

class Account(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hash the password if it is not already hashed
        if self.pk is None or not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)

        # Call the parent save method
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    announcement_image = models.ImageField(upload_to='announcement_image/', blank=True, null=True)

    def __str__(self):
        return self.title

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions", null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="accounts")
    id_number = models.CharField(max_length=50, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(default=timezone.now)
    hire_date = models.DateField(default=timezone.now)
    address = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    tel_number = models.CharField(max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    fingerprint_file = models.FileField(upload_to='fingerprints/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    sss_number = models.CharField(max_length=255, blank=False, null=False, default="")
    time_in = models.TimeField(default=time(9, 0))     
    time_out = models.TimeField(default=time(19, 0))
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
    def calculate_daily_wage(self):
        """
        Calculate and return the daily wage based on the salary.
        Assuming 22 working days in a month.
        """
        working_days_per_month = 22  # Standard working days in a month
        if self.salary > 0:
            return self.salary / working_days_per_month
        return 0.00

    def save(self, *args, **kwargs):
        # Automatically calculate and update daily_wage before saving
        self.daily_wage = self.calculate_daily_wage()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    is_present = models.BooleanField(default=True)
    fingerprint_file = models.FileField(upload_to='attendance_fingerprints/', blank=True, null=True)  # Store the fingerprint file
    picture = models.ImageField(upload_to='attendance_pictures/', blank=True, null=True)
    total_wage = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)

    def __str__(self):
        return f"Attendance for {self.employee} on {self.date}"
    

    def calculate_total_wage(self):
        """
        Calculate the deduction based on lateness.
        """
        if self.time_in and self.employee.time_in:
            # Convert time fields to datetime for comparison
            scheduled_time_in = datetime.combine(self.date, self.employee.time_in)
            actual_time_in = datetime.combine(self.date, self.time_in)

            # Calculate lateness
            if actual_time_in > scheduled_time_in:
                late_minutes = (actual_time_in - scheduled_time_in).total_seconds() / 60
                late_hours = late_minutes // 60
                deduction_rate = 57.00
                deduction = float(late_hours) * float(deduction_rate)

                self.total_wage = float(self.employee.daily_wage) - float(deduction)
            else:
                self.total_wage = self.employee.daily_wage
        else:
            self.total_wage = self.employee.daily_wage

    def save(self, *args, **kwargs):
        # Calculate deduction before saving
        self.calculate_total_wage()
        super().save(*args, **kwargs)

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    start_date = models.DateField()
    end_date = models.DateField()
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def calculate_salary(self):
            # Calculate total hours worked based on attendance records for the period
            attendance_records = Attendance.objects.filter(employee=self.employee, date__range=[self.start_date, self.end_date])
            total_hours = timedelta()

            for attendance in attendance_records:
                if attendance.time_in and attendance.time_out:
                    # Use a reference date to convert time to datetime
                    reference_date = self.start_date
                    
                    # Combine the time with a reference date
                    time_in = datetime.combine(reference_date, attendance.time_in)
                    time_out = datetime.combine(reference_date, attendance.time_out)

                    # If the time_out is before time_in, it means the time is on the next day
                    if time_out < time_in:
                        time_out += timedelta(days=1)

                    # Calculate the difference
                    total_hours += (time_out - time_in)

            # Hourly rate (can be customized based on employee or position)
            hourly_rate = Decimal(self.employee.hourly_rate) if hasattr(self.employee, 'hourly_rate') else 20  
            total_salary = Decimal(total_hours.total_seconds()) / Decimal(3600) * hourly_rate

            # Add allowances, bonuses, and subtract deductions
            self.net_salary = total_salary + self.allowances + self.bonuses - self.deductions
            self.save()

            return self.net_salary

    @property
    def month(self):
        return self.start_date.strftime("%B %Y")

    def __str__(self):
        return f"Payroll for {self.employee} from {self.start_date} to {self.end_date}"

