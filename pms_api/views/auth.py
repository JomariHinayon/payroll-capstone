from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from pms_api.serializer import AccountRegisterSerializer, EmployeeLoginSerializer, AdminLoginSerializer
from core.models import Account, Employee

@extend_schema(tags=["Authentication"])
class AccountRegistrationView(generics.CreateAPIView):
    queryset = Account.objects.all()  # Define the queryset for the view
    serializer_class = AccountRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=201)  

@extend_schema(tags=["Authentication"])
class EmployeeLoginView(APIView):
    serializer_class = EmployeeLoginSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        employee_number = request.data.get('employee_number')
        password = request.data.get('password')
        employee = None
        try:
            # Fetch the employee by employee number
            employee = Employee.objects.get(id_number=employee_number)
            # Fetch the associated user account
            account = Account.objects.get(id=employee.user.id)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Employee number does not exist'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Authenticate the user
        user = authenticate(username=account.username, password=password)
        if user is not None and employee is not None:
            # Generate or retrieve the authentication token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'time_in': employee.time_in,
                'time_out': employee.time_out,
                'username': user.username,
                'employee_number': employee.id_number ,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=["Authentication"])
class AdminLoginView(APIView):
    serializer_class = AdminLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user.is_staff:
            return Response(
                {'error': 'Access denied: Unauthorized login'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Login successful',
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        

@extend_schema(tags=["Authentication"])
class ObtainAuthTokenView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny] 