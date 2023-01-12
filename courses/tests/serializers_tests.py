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
        self.failing_exercise = ExerciseFactory()
        self.failing_submission = SubmissionFactory(
            passed=False, exercise=self.failing_exercise)

        self.completed_exercise = ExerciseFactory()
        self.completed_submission = SubmissionFactory(
            passed=True, exercise=self.completed_exercise)
        return super().setUp()

    def test_progress_data_field(self):
        # No submissions. {is_complete: False, is_in_progress: False}
        exercise = ExerciseFactory()
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserExerciseSerializer(instance=exercise, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # One failing submission. {is_complete: False, is_in_progress: True}
        kwargs = {'context': {'user': self.failing_submission.user}}
        serializer = UserExerciseSerializer(instance=self.failing_exercise, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # One passing submission. {is_complete: True, is_in_progress: False}
        kwargs = {'context': {'user': self.completed_submission.user}}
        serializer = UserExerciseSerializer(
            instance=self.completed_exercise, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two submissions: one failing, one passing. {is_complete: True, is_in_progress: False}
        SubmissionFactory(
            exercise=self.failing_exercise,
            user=self.failing_submission.user,
            passed=True)
        kwargs = {'context': {'user': self.failing_submission.user}}
        serializer = UserExerciseSerializer(instance=self.failing_exercise, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two passing submissions. {is_complete: True, is_in_progress: False}
        SubmissionFactory(
            exercise=self.completed_exercise,
            user=self.completed_submission.user,
            passed=True)
        kwargs = {'context': {'user': self.completed_submission.user}}
        serializer = UserExerciseSerializer(instance=self.completed_exercise, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two failing submissions. {is_complete: False, is_in_progress: True}
        two_failed_subm_exs = ExerciseFactory()
        user = UserFactory()
        SubmissionFactory(
            user=user,
            exercise=two_failed_subm_exs,
            passed=False)
        SubmissionFactory(
            user=user,
            exercise=two_failed_subm_exs,
            passed=False)
        kwargs = {'context': {'user': user}}
        serializer = UserExerciseSerializer(instance=two_failed_subm_exs, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])


class UserLessonSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_lesson = LessonFactory()
        self.complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        self.complete_submission = SubmissionFactory(
            exercise=self.complete_exercise, passed=True)

        self.incomplete_lesson = LessonFactory()
        self.incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=self.incomplete_exercise, passed=False)
        return super().setUp()

    def test_progress_data_field(self):
        # One exercise, but without submissions. {is_complete: False, is_in_progress: False}
        lesson_wo_submissions = LessonFactory()
        ExerciseFactory(lesson=lesson_wo_submissions)
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserLessonSerializer(instance=lesson_wo_submissions, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # One failing submission. {is_complete: False, is_in_progress: True}
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserLessonSerializer(instance=self.incomplete_lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # One passing submission. {is_complete: True, is_in_progress: False}
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserLessonSerializer(instance=self.complete_lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are passing. {is_complete: True, is_in_progress: False}
        second_complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        SubmissionFactory(
            exercise=second_complete_exercise,
            user=self.complete_submission.user,
            passed=True
        )
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserLessonSerializer(instance=self.complete_lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are failing. {is_complete: False, is_in_progress: True}
        second_incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        SubmissionFactory(
            exercise=second_incomplete_exercise,
            user=self.failed_submission.user,
            passed=False
        )
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserLessonSerializer(instance=self.incomplete_lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Three exercises, three submissions: two failing, one passing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        half_complete_lesson = LessonFactory()
        first_exercise = ExerciseFactory(lesson=half_complete_lesson)
        second_exercise = ExerciseFactory(lesson=half_complete_lesson)
        third_exercise = ExerciseFactory(lesson=half_complete_lesson)
        SubmissionFactory(
            exercise=first_exercise,
            user=user,
            passed=False
        )
        SubmissionFactory(
            exercise=second_exercise,
            user=user,
            passed=False
        )
        SubmissionFactory(
            exercise=third_exercise,
            user=user,
            passed=True
        )
        kwargs = {'context': {'user': user}}
        serializer = UserLessonSerializer(instance=half_complete_lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: failing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        lesson = LessonFactory()
        ex1 = ExerciseFactory(lesson=lesson)
        ExerciseFactory(lesson=lesson)
        SubmissionFactory(
            exercise=ex1,
            user=user,
            passed=False
        )
        kwargs = {'context': {'user': user}}
        serializer = UserLessonSerializer(instance=lesson, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: passing. {is_complete: False, is_in_progress: True}
        usr = UserFactory()
        lsn = LessonFactory()
        ex = ExerciseFactory(lesson=lsn)
        ExerciseFactory(lesson=lsn)
        SubmissionFactory(
            exercise=ex,
            user=usr,
            passed=True
        )
        kwargs = {'context': {'user': usr}}
        serializer = UserLessonSerializer(instance=lsn, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])


class UserUnitSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_unit = UnitFactory()
        self.complete_lesson = LessonFactory(unit=self.complete_unit)
        self.complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        self.complete_submission = SubmissionFactory(
            exercise=self.complete_exercise, passed=True)

        self.incomplete_unit = UnitFactory()
        self.incomplete_lesson = LessonFactory(unit=self.incomplete_unit)
        incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_progress_data_field(self):
        # One exercise, but without submissions. {is_complete: False, is_in_progress: False}
        unit_wo_submissions = UnitFactory()
        lesson_wo_submissions = LessonFactory(unit=unit_wo_submissions)
        ExerciseFactory(lesson=lesson_wo_submissions)
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserUnitSerializer(instance=unit_wo_submissions, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # One failing submission. {is_complete: False, is_in_progress: True}
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserUnitSerializer(instance=self.incomplete_unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # One passing submission. {is_complete: True, is_in_progress: False}
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserUnitSerializer(instance=self.complete_unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are passing. {is_complete: True, is_in_progress: False}
        second_complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        SubmissionFactory(
            exercise=second_complete_exercise,
            user=self.complete_submission.user,
            passed=True
        )
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserUnitSerializer(instance=self.complete_unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are failing. {is_complete: False, is_in_progress: True}
        second_incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        SubmissionFactory(
            exercise=second_incomplete_exercise,
            user=self.failed_submission.user,
            passed=False
        )
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserUnitSerializer(instance=self.incomplete_unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Three exercises, three submissions: two failing, one passing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        half_complete_unit = UnitFactory()
        half_complete_lesson = LessonFactory(unit=half_complete_unit)
        another_lesson = LessonFactory(unit=half_complete_unit)
        first_exercise = ExerciseFactory(lesson=half_complete_lesson)
        second_exercise = ExerciseFactory(lesson=half_complete_lesson)
        third_exercise = ExerciseFactory(lesson=another_lesson)
        SubmissionFactory(
            exercise=first_exercise,
            user=user,
            passed=False
        )
        SubmissionFactory(
            exercise=second_exercise,
            user=user,
            passed=False
        )
        SubmissionFactory(
            exercise=third_exercise,
            user=user,
            passed=True
        )
        kwargs = {'context': {'user': user}}
        serializer = UserUnitSerializer(instance=half_complete_unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: failing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        unit = UnitFactory()
        lesson = LessonFactory(unit=unit)
        ex1 = ExerciseFactory(lesson=lesson)
        ExerciseFactory(lesson=lesson)
        SubmissionFactory(
            exercise=ex1,
            user=user,
            passed=False
        )
        kwargs = {'context': {'user': user}}
        serializer = UserUnitSerializer(instance=unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: passing. {is_complete: False, is_in_progress: True}
        usr = UserFactory()
        unit = UnitFactory()
        lsn = LessonFactory(unit=unit)
        ex = ExerciseFactory(lesson=lsn)
        ExerciseFactory(lesson=lsn)
        SubmissionFactory(
            exercise=ex,
            user=usr,
            passed=True
        )
        kwargs = {'context': {'user': usr}}
        serializer = UserUnitSerializer(instance=unit, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])


class UserTrackSerializerTests(TestCase):

    def setUp(self) -> None:
        self.complete_track = TrackFactory()
        self.complete_unit = UnitFactory(track=self.complete_track)
        self.complete_lesson = LessonFactory(unit=self.complete_unit)
        complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        self.complete_submission = SubmissionFactory(
            exercise=complete_exercise, passed=True)

        self.incomplete_track = TrackFactory()
        self.incomplete_unit = UnitFactory(track=self.incomplete_track)
        self.incomplete_lesson = LessonFactory(unit=self.incomplete_unit)
        incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        self.failed_submission = SubmissionFactory(
            exercise=incomplete_exercise, passed=False)
        return super().setUp()

    def test_progress_data_field(self):
        # One exercise, but without submissions. {is_complete: False, is_in_progress: False}
        track_wo_submissions = TrackFactory()
        unit_wo_submissions = UnitFactory(track=track_wo_submissions)
        lesson_wo_submissions = LessonFactory(unit=unit_wo_submissions)
        ExerciseFactory(lesson=lesson_wo_submissions)
        user = UserFactory()
        kwargs = {'context': {'user': user}}
        serializer = UserTrackSerializer(instance=track_wo_submissions, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # One failing submission. {is_complete: False, is_in_progress: True}
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserTrackSerializer(instance=self.incomplete_track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # One passing submission. {is_complete: True, is_in_progress: False}
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserTrackSerializer(instance=self.complete_track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are passing. {is_complete: True, is_in_progress: False}
        second_complete_exercise = ExerciseFactory(lesson=self.complete_lesson)
        SubmissionFactory(
            exercise=second_complete_exercise,
            user=self.complete_submission.user,
            passed=True
        )
        kwargs = {'context': {'user': self.complete_submission.user}}
        serializer = UserTrackSerializer(instance=self.complete_track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertTrue(progress_data['is_complete'])
        self.assertFalse(progress_data['is_in_progress'])

        # Two exercises, two submissions: one both are failing. {is_complete: False, is_in_progress: True}
        second_incomplete_exercise = ExerciseFactory(lesson=self.incomplete_lesson)
        SubmissionFactory(
            exercise=second_incomplete_exercise,
            user=self.failed_submission.user,
            passed=False
        )
        kwargs = {'context': {'user': self.failed_submission.user}}
        serializer = UserTrackSerializer(instance=self.incomplete_track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Three exercises, three submissions: two failing, one passing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        half_complete_track = TrackFactory()
        half_complete_unit1 = UnitFactory(track=half_complete_track)
        half_complete_unit2 = UnitFactory(track=half_complete_track)
        half_complete_lesson = LessonFactory(unit=half_complete_unit1)
        another_lesson = LessonFactory(unit=half_complete_unit2)
        
        first_exercise = ExerciseFactory(lesson=half_complete_lesson)
        second_exercise = ExerciseFactory(lesson=half_complete_lesson)
        third_exercise = ExerciseFactory(lesson=another_lesson)
        fourth_exercise = ExerciseFactory(lesson=another_lesson)
        SubmissionFactory(
            exercise=first_exercise,
            user=user,
            passed=True
        )
        SubmissionFactory(
            exercise=second_exercise,
            user=user,
            passed=False
        )
        SubmissionFactory(
            exercise=third_exercise,
            user=user,
            passed=True
        )
        SubmissionFactory(
            exercise=fourth_exercise,
            user=user,
            passed=False
        )
        kwargs = {'context': {'user': user}}
        serializer = UserTrackSerializer(instance=half_complete_track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: failing. {is_complete: False, is_in_progress: True}
        user = UserFactory()
        track = TrackFactory()
        unit = UnitFactory(track=track)
        lesson = LessonFactory(unit=unit)
        ex1 = ExerciseFactory(lesson=lesson)
        ExerciseFactory(lesson=lesson)
        SubmissionFactory(
            exercise=ex1,
            user=user,
            passed=False
        )
        kwargs = {'context': {'user': user}}
        serializer = UserTrackSerializer(instance=track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])

        # Two exercises, one submission: passing. {is_complete: False, is_in_progress: True}
        usr = UserFactory()
        track = TrackFactory()
        unit = UnitFactory(track=track)
        lsn = LessonFactory(unit=unit)
        ex = ExerciseFactory(lesson=lsn)
        ExerciseFactory(lesson=lsn)
        SubmissionFactory(
            exercise=ex,
            user=usr,
            passed=True
        )
        kwargs = {'context': {'user': usr}}
        serializer = UserTrackSerializer(instance=track, **kwargs)
        progress_data = serializer.data['progress_data']
        self.assertFalse(progress_data['is_complete'])
        self.assertTrue(progress_data['is_in_progress'])
