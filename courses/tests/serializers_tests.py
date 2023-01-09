from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import LessonFactory
from fixtures.factories.courses import SubmissionFactory
from fixtures.factories.courses import UnitFactory

from courses.serializers import UserExerciseSerializer
from courses.serializers import UserLessonSerializer
from courses.serializers import UserUnitSerializer


class UserExerciseSerializerTests(TestCase):

    def test_is_complete_property_field(self):
        exercise = ExerciseFactory()
        not_passed_submission = SubmissionFactory(
            passed=False, exercise=exercise)
        kwargs = {'context': {'user': not_passed_submission.user}}
        serializer = UserExerciseSerializer(instance=exercise, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])

        completed_exercise = ExerciseFactory()
        submission = SubmissionFactory(
            passed=True, exercise=completed_exercise)
        kwargs = {'context': {'user': submission.user}}
        serializer = UserExerciseSerializer(
            instance=completed_exercise, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])


class UserLessonSerializerTests(TestCase):

    def setUp(self) -> None:
        exercise = ExerciseFactory()
        self.submission = SubmissionFactory(exercise=exercise, passed=True)
        self.complete_lesson = LessonFactory()
        exercise.lesson = self.complete_lesson
        exercise.save()

        self.incomplete_lesson = LessonFactory()
        incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_is_complete_property_field(self):
        kwargs = {'context': {'user': self.submission.user}}
        serializer = UserLessonSerializer(instance=self.complete_lesson, **kwargs)
        data = serializer.data
        self.assertTrue(data['is_complete'])

        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserLessonSerializer(
            instance=self.incomplete_lesson, **kwargs)
        data = serializer.data
        self.assertFalse(data['is_complete'])


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
