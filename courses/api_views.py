from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError

from courses.mixins import ReadOnlyOrAdminModelViewSetMixin
from courses.permissions import IsSubmissionOwner
from courses.serializers import TrackSerializer
from courses.serializers import UnitSerializer
from courses.serializers import LessonSerializer
from courses.serializers import ExerciseSerializer
from courses.serializers import SubmissionSerializer
from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise
from courses.models import Submission

from courses.helpers import run_code
from courses.helpers import check_text_source


class TrackViewSet(ReadOnlyOrAdminModelViewSetMixin):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class UnitViewSet(ReadOnlyOrAdminModelViewSetMixin):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class LessonViewSet(ReadOnlyOrAdminModelViewSetMixin):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class ExerciseViewSet(ReadOnlyOrAdminModelViewSetMixin):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        prev = serializer.validated_data.get('previous_exercise')
        self.handle_previous_exercise(prev, instance)
        data = serializer.data
        return Response(serializer.data)

    def handle_previous_exercise(self, prev, instance):
        # Unbind old exercise's next_exercise
        if prev and prev.id == instance.id:
            raise ValidationError(
                'The exercise itself cannot be used as a previous exercise')
        next_of = Exercise.objects.filter(next_exercise__id=instance.id)
        for n in next_of:
            n.next_exercise = None
        Exercise.objects.bulk_update(next_of, ['next_exercise'])
        if prev is not None:
            prev.next_exercise = instance
            prev.save()


class SubmissionViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsSubmissionOwner]

    def perform_create(self, serializer):
        data = serializer.validated_data
        exercise = data.get('exercise')
        submitted_code = data.get('submitted_code', '')
        programming_language = exercise.lesson.unit.track.programming_language
        code = submitted_code + '\n' + (exercise.unit_test if exercise.unit_test else '')
        try:
            is_input_check_correct, error_msg = check_text_source(
                submitted_code,
                exercise.input_should_contain,
                exercise.input_should_not_contain,
                exercise.input_error_text)
            if not is_input_check_correct:
                # if doesn't contain wanted items, return success: false and input_error_text
                # if contains unwanted items, return success: false and output_error_text
                # think about more granular error messages
                serializer.save(output=error_msg, user=self.request.user)
                return

            result = run_code(code, programming_language)
            serializer.save(output=result, user=self.request.user)
        except ValueError as e:
            raise ValidationError({"detail": e})
