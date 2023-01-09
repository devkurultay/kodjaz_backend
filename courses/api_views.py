import markdown as md
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from courses.mixins import ReadOnlyOrAdminModelViewSetMixin
from courses.permissions import IsSubmissionOwner
from courses.serializers import TrackSerializer
from courses.serializers import UnitSerializer
from courses.serializers import LessonSerializer
from courses.serializers import ExerciseSerializer
from courses.serializers import SubmissionSerializer

from courses.serializers import UserExerciseSerializer
from courses.serializers import UserLessonSerializer
from courses.serializers import UserUnitSerializer

from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise
from courses.models import Submission

from courses.helpers import build_input_object
from courses.helpers import Checker


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


class UserTrackViewSet(ReadOnlyModelViewSet):
    serializer_class = TrackSerializer

    def get_queryset(self):
        user = self.request.user
        tracks_ids = Submission.objects.filter(
            user=user
        ).values_list('exercise__lesson__unit__track__id', flat=True).distinct()
        return Track.objects.filter(id__in=tracks_ids)


class UserUnitViewSet(ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UserUnitSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


class UserLessonViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = UserLessonSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


class UserExerciseViewSet(ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = UserExerciseSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


class UserSubmissionViewSet(ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsSubmissionOwner]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(user=user)

    def perform_create(self, serializer):
        data = serializer.validated_data
        exercise = data.get('exercise')
        submitted_code = data.get('submitted_code', '')
        try:
            check_input = build_input_object(exercise, submitted_code)
            checker = Checker(check_input)
            check_result = checker.check()
            is_success = check_result['success']
            console_output = check_result['console_output']
            error_message = check_result['error_msg']
            error_html = md.markdown(error_message)
            # TODO(murat): test exceptions
            serializer.save(
                passed=is_success,
                console_output=console_output,
                error_message=error_html,
                user=self.request.user)
        except ValueError as e:
            raise ValidationError({"detail": e})
