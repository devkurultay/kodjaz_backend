from rest_framework.viewsets import ModelViewSet

from courses.serializers import TrackSerializer
from courses.models import Track


class TracksViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
