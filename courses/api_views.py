from rest_framework.response import Response
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        prev = serializer.validated_data.get('previous_exercise')
        if prev:
            self.handle_previous_exercise(prev, instance)
        data = serializer.data
        return Response(serializer.data)

    def handle_previous_exercise(self, prev, instance):
        # Unbind old exercise's next_exercise
        next_of = Exercise.objects.filter(next_exercise__id=instance.id)
        for n in next_of:
            n.next_exercise = None
        Exercise.objects.bulk_update(next_of, ['next_exercise'])
        prev.next_exercise = instance
        prev.save()
