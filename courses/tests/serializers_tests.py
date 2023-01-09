from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import LessonFactory
from fixtures.factories.courses import SubmissionFactory
from fixtures.factories.courses import UnitFactory
from fixtures.factories.courses import TrackFactory
from fixtures.factories.user import UserFactory

from courses.serializers import UserExerciseSerializer
from courses.serializers import UserLessonSerializer
from courses.serializers import UserUnitSerializer
from courses.serializers import UserTrackSerializer


class UserExerciseSerializerTests(TestCase):

    def setUp(self) -> None:
        self.exercise = ExerciseFactory()
        self.not_passed_submission = SubmissionFactory(
            passed=False, exercise=self.exercise)
        
        self.completed_exercise = ExerciseFactory()
        self.submission = SubmissionFactory(
            passed=True, exercise=self.completed_exercise)
        return super().setUp()

    def test_is_complete_field(self):
        kwargs = {'context': {'user': self.not_passed_submission.user}}
        serializer = UserExerciseSerializer(instance=self.exercise, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])

        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserExerciseSerializer(
            instance=self.completed_exercise, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])
    
    def test_is_in_progress_field(self):
        # When only one submission: passed = False
        kwargs = {'context': {'user': self.not_passed_submission.user}}
        serializer = UserExerciseSerializer(instance=self.exercise, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_in_progress'])

        # When added another submission: passed = True
        SubmissionFactory(
            passed=True, exercise=self.exercise,
            user=self.not_passed_submission.user)
        serializer = UserExerciseSerializer(instance=self.exercise, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_in_progress'])

        # When an exercise does not have any submissions
        exercise = ExerciseFactory()
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserExerciseSerializer(instance=exercise, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_in_progress'])


class UserLessonSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_lesson = LessonFactory()
        exercise = ExerciseFactory(lesson=self.complete_lesson)
        self.submission = SubmissionFactory(exercise=exercise, passed=True)

        self.incomplete_lesson = LessonFactory()
        incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_is_complete_field(self):
        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserLessonSerializer(instance=self.complete_lesson, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])

        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserLessonSerializer(
            instance=self.incomplete_lesson, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])
    
    def test_is_in_progress_field(self):
        # When only one submission: passed = False
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserLessonSerializer(instance=self.incomplete_lesson, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_in_progress'])

        # When only one submission: passed = True
        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserLessonSerializer(instance=self.complete_lesson, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_in_progress'])

        # When an exercise does not have any submissions
        lesson = LessonFactory()
        ExerciseFactory(lesson=lesson)
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserLessonSerializer(instance=lesson, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_in_progress'])


class UserUnitSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_unit = UnitFactory()
        complete_lesson = LessonFactory(unit=self.complete_unit)
        exercise = ExerciseFactory(lesson=complete_lesson)
        self.submission = SubmissionFactory(exercise=exercise, passed=True)

        self.incomplete_unit = UnitFactory()
        incomplete_lesson = LessonFactory(unit=self.incomplete_unit)
        incomplete_exercise = ExerciseFactory(lesson=incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_is_complete_property_field(self):
        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserUnitSerializer(instance=self.complete_unit, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])

        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserUnitSerializer(
            instance=self.incomplete_unit, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])


class UserTrackSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_track = TrackFactory()
        complete_unit = UnitFactory(track=self.complete_track)
        complete_lesson = LessonFactory(unit=complete_unit)
        exercise = ExerciseFactory(lesson=complete_lesson)
        self.submission = SubmissionFactory(exercise=exercise, passed=True)

        self.incomplete_track = TrackFactory()
        incomplete_unit = UnitFactory(track=self.incomplete_track)
        incomplete_lesson = LessonFactory(unit=incomplete_unit)
        incomplete_exercise = ExerciseFactory(lesson=incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_is_complete_property_field(self):
        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserTrackSerializer(instance=self.complete_track, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])

        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserTrackSerializer(
            instance=self.incomplete_track, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])
