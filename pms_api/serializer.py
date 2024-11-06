from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from core.models import Account, Employee, Attendance, Payroll, Department, Position


class EmployeeLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    employee_number = serializers.CharField(required=False, allow_null=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('employee_number', 'password', 'token')

    def validate(self, attrs):
        employee_number = attrs.get('employee_number')
        password = attrs.get('password')
        
        employee = get_object_or_404(Employee, id_number=employee_number)

        if employee:
            try:
                account = authenticate(employee_number=employee_number, password=password)
                token, created = Token.objects.get_or_create(user=account)
                
                # Add the token to the serializer's validated data
                attrs['token'] = token.key
                return attrs
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Account does not exist.")
        else:
            raise serializers.ValidationError("Invalid employee number or password.")
        
class AdminLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'token')

class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    employee_number = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'first_name', 'last_name', 'employee_number')

    def create(self, validated_data):
        password = validated_data.pop('password')
        employee_number = validated_data.pop('employee_number', None)

        # Create the Account
        account, created = Account.objects.get_or_create(**validated_data)

        # If employee_number is provided, link to existing Employee or create a new one
        if employee_number:
            # Check if the employee already exists
            try:
                employee = Employee.objects.get(id_number=employee_number)
                employee.user = account
                employee.save()
            except Employee.DoesNotExist:
                # Create a new Employee if employee_number is not provided
                    employee = Employee.objects.create(
                        user=account,
                        id_number=employee_number,
                        gender="M", 
                        is_active=False
                    )
                    employee.save()

        return account
    

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['title']

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'id_number', 'user', 'gender', 'birth_date', 'hire_date', 
            'address', 'department', 'position', 'phone_number', 
            'tel_number', 'salary', 'is_active', 'full_name'  # Include full_name in fields
        ]

    def get_full_name(self, obj):
        # Combine first_name and last_name
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None
    
class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'date', 'time_in', 'time_out', 
            'is_present', 'fingerprint_data'
        ]
        read_only_fields = ['id']


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'start_date', 'end_date', 'deductions', 'allowances', 'bonuses']
        read_only_fields = ['id', 'net_salary']
    
    def create(self, validated_data):
        payroll = Payroll(**validated_data)
        payroll.calculate_net_salary()  # Calculate net salary before saving
        payroll.save()
        return payroll

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.calculate_net_salary()  # Recalculate net salary before saving
        instance.save()
        return instance