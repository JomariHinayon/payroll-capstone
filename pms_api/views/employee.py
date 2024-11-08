from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db import transaction

from core.models import Employee, Attendance, Account
from pms_api.serializer import EmployeeSerializer, AttendanceSerializer

import json

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
import json

@extend_schema(tags=["Employee"])
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['post'])
    def create_with_user(self, request):
        """
        This view creates both a User and an Employee in one API call.
        """
        dict_data = request.data.dict()

        json_data_str = dict_data['json_data']  # Get the JSON string
        json_data = json.loads(json_data_str)

        profile_image = dict_data.get('profile_image')
        fingerprint_file = dict_data.get('fingerprint_file')

        try:
            # Start a transaction to ensure both user and employee are created atomically
            with transaction.atomic():
                # Create the employee with user
                employee_serializer = EmployeeSerializer(data=json_data)

                if employee_serializer.is_valid():
                    # Save the employee (this will also create the user)
                    employee = employee_serializer.save()

                    # Handle profile image if provided
                    if profile_image:
                        employee.profile_image = profile_image
                        employee.save()

                    # Handle fingerprint if provided
                    if fingerprint_file:
                        # Save the fingerprint file
                        employee.fingerprint_file = fingerprint_file
                        employee.save()

                    return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
