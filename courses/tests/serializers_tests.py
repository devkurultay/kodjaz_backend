from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import SubmissionFactory

from courses.serializers import ExerciseSerializer


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
