from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AccountRegistrationView, AccountLoginView, ObtainAuthTokenView, EmployeeViewSet, AttendanceViewSet, PayrollViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'payroll', PayrollViewSet)


urlpatterns = [
    # auth
    path('get-token/', ObtainAuthTokenView.as_view(), name='api_get_token'),
    path('register/', AccountRegistrationView.as_view(), name='api_register'),
    path('login/', AccountLoginView.as_view(), name='login'),

    # router
    path('', include(router.urls)),
]
