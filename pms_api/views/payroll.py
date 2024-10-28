from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from core.models import Payroll
from pms_api.serializer import PayrollSerializer


@extend_schema(tags=["Payroll"])
class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer