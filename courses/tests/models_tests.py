from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import SubmissionFactory


class ExerciseTests(TestCase):

    def test_is_complete_property(self):
        exercise = ExerciseFactory()
        self.assertFalse(exercise.is_complete)
        submission = SubmissionFactory()
        # Check if the submission is `passed = True`
        self.assertTrue(submission.passed)
        submission.exercise = exercise
        submission.save()
        # Check if the submission is `passed = True`
        # then is_complete is also True
        self.assertTrue(exercise.is_complete)
