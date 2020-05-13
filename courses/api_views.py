from rest_framework.generics import ListCreateAPIView

from courses.serializers import TrackSerializer
from courses.models import Track


class TracksList(ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
