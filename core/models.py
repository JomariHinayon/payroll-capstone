from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from config import settings
from django.utils import timezone


class Account(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions")
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
    birth_date = models.DateField()
    hire_date = models.DateField()
    address = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="employees")
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    tel_number = models.CharField(max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    is_present = models.BooleanField(default=True)
    fingerprint_data = models.BinaryField(blank=True, null=True)  
    picture = models.ImageField(upload_to='attendance_pictures/', blank=True, null=True) 

    def __str__(self):
        return f"Attendance for {self.employee} on {self.date}"

class SalaryStructure(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salary_structures")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    effective_date = models.DateField()

    def __str__(self):
        return f"Salary Structure for {self.employee}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    start_date = models.DateField()
    end_date = models.DateField()
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name="payrolls")
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_net_salary(self):
        self.net_salary = self.base_salary + self.allowances + self.bonuses - self.deductions
        return self.net_salary

    def __str__(self):
        return f"Payroll for {self.employee} from {self.start_date} to {self.end_date}"