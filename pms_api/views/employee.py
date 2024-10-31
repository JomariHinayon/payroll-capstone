from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.models import Employee, Attendance
from pms_api.serializer import EmployeeSerializer, AttendanceSerializer

@extend_schema(tags=["Employee"])
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer