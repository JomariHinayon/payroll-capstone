from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Employee, Attendance

from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from core.models import Payroll
from django.utils.timezone import now


def calculate_salary_view(request, employee_id):
    try:
        # Find the employee by ID
        employee = Employee.objects.get(id=employee_id)
        
        try:
            # Find the employee by ID
            employee = Employee.objects.get(id=employee_id)

            today = now().date()  # current date
            start_date = today.replace(day=1)  # first day of the current month

            # Get the current date as the end date
            end_date = today  # current date

            # Create payroll for the employee
            payroll = Payroll.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,
                allowances=2000,  
                deductions=500,  
                bonuses=1000,
                net_salary=0,
            )
            # Calculate the net salary and save it
            payroll.calculate_salary()

            # Success message
            messages.success(request, f"Payroll for {employee.user.first_name} {employee.user.last_name} has been generated.")
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found.")

        messages.success(request, f"Salary for {employee.user.first_name} {employee.user.last_name} has been calculated.")
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found.")
    
    # Redirect back to the admin page after the calculation
    return redirect('/admin/')