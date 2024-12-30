from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from core.models import Announcement
from pms_api.serializer import AnnouncementSerializer

@extend_schema(tags=["Announcements"])
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer