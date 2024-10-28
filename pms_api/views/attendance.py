from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from core.models import Attendance
from pms_api.serializer import AttendanceSerializer

@extend_schema(tags=["Attendance"])
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer