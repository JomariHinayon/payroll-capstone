from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from core.models import Employee, Attendance
from pms_api.serializer import EmployeeSerializer, AttendanceSerializer

@extend_schema(tags=["Employee"])
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
