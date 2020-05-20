from rest_framework.viewsets import ModelViewSet

from courses.serializers import TrackSerializer, UnitSerializer, LessonSerializer, ExerciseSerializer
from courses.models import Track, Unit, Lesson, Exercise


class TracksViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ExerciseViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
