from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.dateparse import parse_time
from rest_framework.decorators import action

from core.models import Attendance, Employee
from pms_api.serializer import AttendanceSerializer
import json, base64, logging, hashlib

logger = logging.getLogger(__name__)


def generate_fingerprint_hash(fingerprint_data):
    """Generate a hash from fingerprint data for reliable comparison."""
    return hashlib.sha256(fingerprint_data).hexdigest()

@extend_schema(tags=["Attendance"])
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['post'])
    def create_attendance(self, request):
        # Extract fingerprint and other parameters
        dict_data = request.data.dict()
        json_data_str = dict_data.get('json_data', '{}')
        json_data = json.loads(json_data_str)

        fingerprint_file = request.FILES.get("fingerprint_file")
        if fingerprint_file:
            fingerprint_data = fingerprint_file.read()
            input_fingerprint_hash = generate_fingerprint_hash(fingerprint_data)
        else:
            return Response({"detail": "Fingerprint file is required."}, status=status.HTTP_400_BAD_REQUEST)

        date = json_data.get('date')
        time_in = json_data.get('time_in')
        time_out = json_data.get('time_out')

        try:
            # Step 1: Find the employee by comparing fingerprint hashes
            matching_employee = None
            for employee in Employee.objects.all():
                if employee.fingerprint_file:
                    with open(employee.fingerprint_file.path, 'rb') as f:
                        employee_fingerprint = f.read()
                        employee_fingerprint_hash = generate_fingerprint_hash(employee_fingerprint)

                    # Compare hashes instead of raw binary data
                    print(employee.user.username)
                    print(input_fingerprint_hash)
                    print("===")
                    print(employee_fingerprint_hash)
                    print("================================")
                    if input_fingerprint_hash == employee_fingerprint_hash:
                        matching_employee = employee
                        break

            if not matching_employee:
                return Response({"detail": "Fingerprint not recognized."}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Create attendance record for matched employee
            attendance = Attendance.objects.create(
                employee=matching_employee,
                date=date,
                time_in=parse_time(time_in),
                time_out=parse_time(time_out),
                is_present=True,
                fingerprint_file=fingerprint_file  # Store the fingerprint file
            )

            # Step 3: Serialize and respond
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception during attendance creation: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)