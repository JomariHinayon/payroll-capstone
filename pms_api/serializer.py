from rest_framework import serializers
from core.models import Account, Employee, Attendance, Payroll

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password')

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
            'is_present', 'fingerprint_data', 'picture'
        ]
        read_only_fields = ['id']


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'start_date', 'end_date', 'salary_structure', 
            'allowances', 'deductions', 'bonuses', 'net_salary'
        ]
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