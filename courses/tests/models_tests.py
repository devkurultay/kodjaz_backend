from django.test.testcases import TestCase
from fixtures.factories.courses import ExerciseFactory
from fixtures.factories.courses import LessonFactory
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


class LessonTests(TestCase):
    def setUp(self):
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

    def test_is_complete_property(self):
        self.assertTrue(self.complete_lesson.is_complete)
        self.assertFalse(self.incomplete_lesson.is_complete)
