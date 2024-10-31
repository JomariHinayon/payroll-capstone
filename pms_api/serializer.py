from rest_framework import serializers
from core.models import Account, Employee, Attendance, Payroll, Department, Position

class AccountSerializer(serializers.ModelSerializer):
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

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'id_number', 'user', 'gender', 'birth_date', 'hire_date', 'address', 'department', 'position', 
            'phone_number', 'tel_number', 'salary', 'is_active'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
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