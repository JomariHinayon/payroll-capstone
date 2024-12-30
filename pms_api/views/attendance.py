from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.dateparse import parse_time, parse_date
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

        username = json_data.get('username')
        date_str = json_data.get('date')
        time_in_str = json_data.get('time_in', None)
        time_out_str = json_data.get('time_out', None)
        picture = json_data.get('picture', None)
        employee_fingerprint = None
        error_message = None

        print(json_data)
        try:
            # Convert `date` to `datetime.date`
            date = parse_date(date_str)
            if not date:
                raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
            
            if not picture:
                raise ValueError("No attendance picture. Please take a pic.")

            # Convert `time_in` and `time_out` to `datetime.time`
            time_in = parse_time(time_in_str) if time_in_str else None
            time_out = parse_time(time_out_str) if time_out_str else None
            
            # Use `user__username` to look up the Employee based on the User model's username field
            employee = Employee.objects.get(user__username=username)

            # Check if an attendance record for the same employee already exists for the current day
            existing_attendance = Attendance.objects.filter(employee=employee, date=date).first()

            if existing_attendance:
                # If an attendance record already exists for this employee on the given date
                error_message = f"Attendance for employee '{username}' on {date} already exists."
                logger.warning(error_message)
                return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

            # Create attendance record for matched employee
            attendance = Attendance.objects.create(
                employee=employee,
                date=date,
                time_in=time_in,
                time_out=time_out,
                is_present=True,
                fingerprint_file=employee_fingerprint  # Store the fingerprint file
            )

            # Serialize and respond
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Employee.DoesNotExist:
            error_message = f"Employee with username '{username}' does not exist."
            logger.error(error_message)
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception during attendance creation: {str(e)}")
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
