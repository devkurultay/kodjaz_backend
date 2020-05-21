from rest_framework.viewsets import ModelViewSet

from courses.serializers import TrackSerializer
from courses.serializers import UnitSerializer
from courses.serializers import LessonSerializer
from courses.serializers import ExerciseSerializer
from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise


class TrackViewSet(ModelViewSet):
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
