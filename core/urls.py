from django.urls import path, include

from .views import calculate_salary_view

urlpatterns = [
    # Your other URLs...
    path('calculate_salary/<int:employee_id>/', calculate_salary_view, name='calculate_salary'),
]