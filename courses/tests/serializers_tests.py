from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import LessonFactory
from fixtures.factories.courses import SubmissionFactory

from courses.serializers import ExerciseSerializer
from courses.serializers import LessonSerializer


class ExerciseSerializerTests(TestCase):

    def test_is_complete_property_field(self):
        exercise = ExerciseFactory()
        # factory instance has `is_complete = False`
        self.assertFalse(exercise.is_complete)
        serializer = ExerciseSerializer(instance=exercise)
        data = serializer.data
        self.assertFalse(data['is_complete'])

        submission = SubmissionFactory()
        # factory instance has `passed = True`
        self.assertTrue(submission.passed)
        submission.exercise = exercise
        submission.save()
        # since new submission is added, `is_complete = True`
        self.assertTrue(exercise.is_complete)

        serializer = ExerciseSerializer(instance=exercise)
        data = serializer.data
        self.assertTrue(data['is_complete'])


class LessonSerializerTests(TestCase):

    def setUp(self) -> None:
        exercise = ExerciseFactory()
        submission = SubmissionFactory()
        submission.exercise = exercise
        submission.save()
        self.complete_lesson = LessonFactory()
        exercise.lesson = self.complete_lesson
        exercise.save()

        self.incomplete_lesson = LessonFactory()
        incomplete_exercise = ExerciseFactory()
        incomplete_exercise.lesson = self.incomplete_lesson
        incomplete_exercise.save()
        return super().setUp()

    def test_is_complete_property_field(self):
        serializer = LessonSerializer(instance=self.complete_lesson)
        data = serializer.data
        self.assertTrue(data['is_complete'])

        serializer = LessonSerializer(instance=self.incomplete_lesson)
        data = serializer.data
        self.assertFalse(data['is_complete'])
