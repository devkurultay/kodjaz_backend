from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.db.models import F
from django.db.models import Exists
from django.db.models import ExpressionWrapper
from django.db.models import OuterRef
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models.lookups import GreaterThan
from django.db.models.lookups import Exact
from django.utils.translation import gettext_lazy as _
from users.models import User


class Badge(models.Model):
    name = models.CharField(_('Name of a Badge'), max_length=255)
    is_published = models.BooleanField()
    date_time_created = models.DateTimeField(_('Badge Creation Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Badge Modification Date and Time'), auto_now=True)


class Track(models.Model):
    name = models.CharField(_('Name of a Track'), max_length=255)
    description = models.CharField(_('Description of a Track'), max_length=255)
    is_published = models.BooleanField()
    date_time_created = models.DateTimeField(_('Track Creation Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Track Modification Date and Time'), auto_now=True)
    programming_language = models.CharField(_('Programming language name'), max_length=255)

    def __str__(self):
        return self.name

    @property
    def unit_lessons_duration(self):
        return self.track_units.filter(is_published=True).aggregate(
            Sum('unit_lessons__lesson_exercises__duration'))['unit_lessons__lesson_exercises__duration__sum']

    @property
    def units_count(self):
        return self.track_units.filter(is_published=True).count()

    @property
    def lessons_count(self):
        units = self.track_units.filter(is_published=True)
        return sum([u.lessons_count for u in units])

    def get_progress_data(self, user):
        not_passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=False,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=True,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        in_progress_exp = GreaterThan(
            F('not_passed_submissions_count'), 0) & Exact(F('passed_submissions_count'), 0)
        in_progress = ExpressionWrapper(in_progress_exp, output_field=models.BooleanField())

        submissions_sum = F('passed_submissions_count') + F('not_passed_submissions_count')

        exercise_template_subq = Exercise.objects.annotate(
            not_passed_submissions_count=Coalesce(not_passed_submissions_count, 0)
        ).annotate(
            passed_submissions_count=Coalesce(passed_submissions_count, 0)
        ).annotate(
            has_submissions=GreaterThan(submissions_sum,  0)
        ).annotate(
            is_complete=GreaterThan(F('passed_submissions_count'),  0)
        ).annotate(
            is_in_progress=in_progress
        ).filter(lesson__unit__track=OuterRef('pk'))

        no_submissions = Q(has_submissions=False)
        has_passed_submissions = Q(passed_submissions_count__gt=0)
        has_failed_submissions = Q(not_passed_submissions_count__gt=0)

        # `is_complete` if the following does not exist:
        # (is_in_progress=True and is_complete=False) OR
        # no_submissions
        complete_expr = (
            Q(is_in_progress=True) & Q(is_complete=False)) | no_submissions

        # ((has_failed_submissions OR has_passed_submissions) AND no_submissions_q) OR
        # (has_failed_submissions AND has_passed_submissions) OR
        # (has_failed_submissions AND (~has_passed_submissions AND ~no_submissions_q))
        has_passed_or_failed_q = Exists(
            exercise_template_subq.filter(has_failed_submissions | has_passed_submissions))
        has_no_submissions_q = Exists(exercise_template_subq.filter(no_submissions))
        has_subm_and_exs_wo_submissions = has_passed_or_failed_q & has_no_submissions_q

        has_failed_submissions_q = Exists(exercise_template_subq.filter(has_failed_submissions))
        has_passed_submissions_q = Exists(exercise_template_subq.filter(has_passed_submissions))
        has_failed_and_passed_subm = has_failed_submissions_q & has_passed_submissions_q

        has_only_failed = has_failed_submissions_q & ~has_passed_submissions_q & ~has_no_submissions_q

        in_progress_expr = has_subm_and_exs_wo_submissions | has_failed_and_passed_subm | has_only_failed

        track = Track.objects.annotate(
            is_complete=~Exists(exercise_template_subq.filter(complete_expr)) # NOT EXISTS
        ).annotate(
            is_in_progress=in_progress_expr
        ).get(id=self.id)
        return {'is_complete': track.is_complete, 'is_in_progress': track.is_in_progress}


class Unit(models.Model):
    name = models.CharField(_('Name of a Unit'), max_length=255)
    description = models.CharField(_('Description of a Unit'), max_length=255)
    is_published = models.BooleanField()
    track = models.ForeignKey(Track, related_name='track_units', on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(_('Unit Creation Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Unit Modification Date and Time'), auto_now=True)

    def __str__(self):
        return self.name

    @property
    def lessons_exercises_duration(self):
        return self.unit_lessons.filter(is_published=True).aggregate(
            Sum('lesson_exercises__duration'))['lesson_exercises__duration__sum']

    @property
    def lessons_count(self):
        return self.unit_lessons.filter(is_published=True).count()

    def get_progress_data(self, user):
        not_passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=False,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=True,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        in_progress_exp = GreaterThan(
            F('not_passed_submissions_count'), 0) & Exact(F('passed_submissions_count'), 0)
        in_progress = ExpressionWrapper(in_progress_exp, output_field=models.BooleanField())

        submissions_sum = F('passed_submissions_count') + F('not_passed_submissions_count')

        exercise_template_subq = Exercise.objects.annotate(
            not_passed_submissions_count=Coalesce(not_passed_submissions_count, 0)
        ).annotate(
            passed_submissions_count=Coalesce(passed_submissions_count, 0)
        ).annotate(
            has_submissions=GreaterThan(submissions_sum,  0)
        ).annotate(
            is_complete=GreaterThan(F('passed_submissions_count'),  0)
        ).annotate(
            is_in_progress=in_progress
        ).filter(lesson__unit=OuterRef('pk'))

        no_submissions = Q(has_submissions=False)
        has_passed_submissions = Q(passed_submissions_count__gt=0)
        has_failed_submissions = Q(not_passed_submissions_count__gt=0)

        # `is_complete` if the following does not exist:
        # (is_in_progress=True and is_complete=False) OR
        # no_submissions
        complete_expr = (
            Q(is_in_progress=True) & Q(is_complete=False)) | no_submissions

        # ((has_failed_submissions OR has_passed_submissions) AND no_submissions_q) OR
        # (has_failed_submissions AND has_passed_submissions) OR
        # (has_failed_submissions AND (~has_passed_submissions AND ~no_submissions_q))
        has_passed_or_failed_q = Exists(
            exercise_template_subq.filter(has_failed_submissions | has_passed_submissions))
        has_no_submissions_q = Exists(exercise_template_subq.filter(no_submissions))
        has_subm_and_exs_wo_submissions = has_passed_or_failed_q & has_no_submissions_q

        has_failed_submissions_q = Exists(exercise_template_subq.filter(has_failed_submissions))
        has_passed_submissions_q = Exists(exercise_template_subq.filter(has_passed_submissions))
        has_failed_and_passed_subm = has_failed_submissions_q & has_passed_submissions_q

        has_only_failed = has_failed_submissions_q & ~has_passed_submissions_q & ~has_no_submissions_q

        in_progress_expr = has_subm_and_exs_wo_submissions | has_failed_and_passed_subm | has_only_failed

        unit = Unit.objects.annotate(
            is_complete=~Exists(exercise_template_subq.filter(complete_expr)) # NOT EXISTS
        ).annotate(
            is_in_progress=in_progress_expr
        ).get(id=self.id)
        return {'is_complete': unit.is_complete, 'is_in_progress': unit.is_in_progress}


class Lesson(models.Model):
    name = models.CharField(_('Name of a Lesson'), max_length=255)
    is_published = models.BooleanField()
    unit = models.ForeignKey(Unit, related_name='unit_lessons', on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, null=True, blank=True, related_name='lesson_badge', on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(_('Lesson Creation Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Lesson Modification Date and Time'), auto_now=True)

    def __str__(self):
        return self.name

    @property
    def exercises_duration(self):
        return self.lesson_exercises.filter(is_published=True).aggregate(Sum('duration'))['duration__sum']

    @property
    def exercises_number(self):
        return self.lesson_exercises.filter(is_published=True).count()

    def get_progress_data(self, user):
        not_passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=False,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=True,
                exercise_submission__user=user,
            ),
            distinct=True
        )
        in_progress_exp = GreaterThan(
            F('not_passed_submissions_count'), 0) & Exact(F('passed_submissions_count'), 0)
        in_progress = ExpressionWrapper(in_progress_exp, output_field=models.BooleanField())

        submissions_sum = F('passed_submissions_count') + F('not_passed_submissions_count')

        exercise_template_subq = Exercise.objects.annotate(
            not_passed_submissions_count=Coalesce(not_passed_submissions_count, 0)
        ).annotate(
            passed_submissions_count=Coalesce(passed_submissions_count, 0)
        ).annotate(
            has_submissions=GreaterThan(submissions_sum,  0)
        ).annotate(
            is_complete=GreaterThan(F('passed_submissions_count'),  0)
        ).annotate(
            is_in_progress=in_progress
        ).filter(lesson=OuterRef('pk'))

        no_submissions = Q(has_submissions=False)
        has_passed_submissions = Q(passed_submissions_count__gt=0)
        has_failed_submissions = Q(not_passed_submissions_count__gt=0)

        # `is_complete` if the following does not exist:
        # (is_in_progress=True and is_complete=False) OR
        # (is_in_progress=False and is_complete=False)
        complete_expr = (
            Q(is_in_progress=True) & Q(is_complete=False)) | no_submissions

        # ((has_failed_submissions OR has_passed_submissions) AND no_submissions_q) OR
        # (has_failed_submissions AND has_passed_submissions) OR
        # (has_failed_submissions AND (~has_passed_submissions AND ~no_submissions_q))
        has_passed_or_failed_q = Exists(
            exercise_template_subq.filter(has_failed_submissions | has_passed_submissions))
        has_no_submissions_q = Exists(exercise_template_subq.filter(no_submissions))
        has_subm_and_exs_wo_submissions = has_passed_or_failed_q & has_no_submissions_q

        has_failed_submissions_q = Exists(exercise_template_subq.filter(has_failed_submissions))
        has_passed_submissions_q = Exists(exercise_template_subq.filter(has_passed_submissions))
        has_failed_and_passed_subm = has_failed_submissions_q & has_passed_submissions_q

        has_only_failed = has_failed_submissions_q & ~has_passed_submissions_q & ~has_no_submissions_q

        in_progress_expr = has_subm_and_exs_wo_submissions | has_failed_and_passed_subm | has_only_failed

        lsn = Lesson.objects.annotate(
            is_complete=~Exists(exercise_template_subq.filter(complete_expr)) # NOT EXISTS
        ).annotate(
            is_in_progress=in_progress_expr
        ).get(id=self.id)
        return {'is_complete': lsn.is_complete, 'is_in_progress': lsn.is_in_progress}


CHECKER_HELP_TEXT = _('separate with comma, without spaces, like this: my_var,hello world')


class Exercise(models.Model):
    name = models.CharField(_('Name of an Exercise'), max_length=255)
    lecture = models.TextField(_('Lecture Text'))
    instruction = models.TextField(_('Instruction Text'))
    hint = models.TextField(_('Hint on how to solve the task'), blank=True, null=True)
    default_code = models.TextField(_('Default Code'), blank=True)
    duration = models.PositiveSmallIntegerField(_('Exercise duration in minutes'), default=0, blank=True)
    input_should_contain = models.CharField(
        _('List of keywords which should be presented in the submitted code'),
        help_text=CHECKER_HELP_TEXT,
        blank=True,
        max_length=255)
    input_should_contain_error_msg = models.CharField(
        _("Error text shown when the input does not contain a required item"), blank=True, max_length=255)
    input_should_not_contain = models.CharField(
        _('List of keywords which should NOT be presented in the submitted code'),
        help_text=CHECKER_HELP_TEXT,
        blank=True,
        max_length=255)
    input_should_not_contain_error_msg = models.CharField(
        _("Error text shown when the input contains an unwanted item"), blank=True, max_length=255)
    # TODO(murat): remove this field after migration
    input_error_text = models.CharField(
        _("Error text shown when expected input was not found in the written code"), blank=True, max_length=255)
    output_should_contain = models.CharField(
        _("List of keywords which should be presented in the output"),
        help_text=CHECKER_HELP_TEXT,
        blank=True,
        max_length=255)
    output_should_contain_error_msg = models.CharField(
        _("Error text shown when the output does not contain a required item"), blank=True, max_length=255)
    output_should_not_contain = models.CharField(
        _("List of keywords which should NOT be presented in the output"),
        help_text=CHECKER_HELP_TEXT,
        blank=True,
        max_length=255)
    output_should_not_contain_error_msg = models.CharField(
        _("Error text shown when the output contains an unwanted item"), blank=True, max_length=255)
    # TODO(murat): remove this field after migration
    output_error_text = models.CharField(
        _("Error text shown when expected output doesn't show up"), blank=True, max_length=255)
    unit_test = models.TextField(_('Code for testing with unit tests'), blank=True)
    next_exercise = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    karma = models.PositiveSmallIntegerField(_('Point to be given for passing the current exercise'), default=1)
    is_published = models.BooleanField()
    lesson = models.ForeignKey(Lesson, related_name='lesson_exercises', on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(_('Exercise Creation Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Exercise Modification Date and Time'), auto_now=True)
    text_file_content = models.TextField(_('If this field has a content, file.txt tab will be shown'), blank=True)

    def __str__(self):
        return self.name

    @property
    def unit_id(self):
        return self.lesson.unit.id

    @property
    def track_id(self):
        return self.lesson.unit.track.id

    def get_progress_data(self, user):
        not_passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=False,
                exercise_submission__user=user,
            )
        )
        passed_submissions_count = Count(
            'exercise_submission',
            filter=Q(
                exercise_submission__passed=True,
                exercise_submission__user=user,
            )
        )
        in_progress_exp = GreaterThan(
            F('not_passed_submissions_count'), 0) & Exact(F('passed_submissions_count'), 0)
        in_progress = ExpressionWrapper(in_progress_exp, output_field=models.BooleanField())
        ex = Exercise.objects.annotate(
            not_passed_submissions_count=not_passed_submissions_count
        ).annotate(
            passed_submissions_count=passed_submissions_count
        ).annotate(
            is_complete=GreaterThan(F('passed_submissions_count'),  0)
        ).annotate(
            is_in_progress=in_progress
        ).get(id=self.id)
        return {'is_complete': ex.is_complete, 'is_in_progress': ex.is_in_progress}


class SubmissionCreationException(Exception):
    pass


class Submission(models.Model):
    user = models.ForeignKey(User, related_name='user_submission', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='exercise_submission', on_delete=models.CASCADE)
    submitted_code = models.TextField(_('Submitted code'), blank=True)
    console_output = models.TextField(_('Result'), blank=True)
    karma = models.PositiveSmallIntegerField(_('Gained points'), default=0)
    failed_attempts = models.PositiveIntegerField(_('Amount of attempts user failed to pass the exercise'),
                                                  blank=True, default=0)
    date_time_created = models.DateTimeField(_('Submission Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(_('Submission Modification Date and Time'), auto_now=True)
    passed = models.BooleanField(default=False)
    error_message = models.TextField(_('Error message'), blank=True)

    def __str__(self):
        return 'Submission: {}. Exercise: {}. User: {}'.format(
            self.id,
            self.exercise,
            self.user
        )

    @classmethod
    def create_from_exercise(cls, user, exercise, submitted_code, text_file_content, passed):
        try:
            obj = cls.objects.create(user=user, exercise=exercise)
            obj.submitted_code = submitted_code
            obj.text_file_content = text_file_content
            obj.karma = exercise.karma if passed else 0
            obj.failed_attempts += 0 if passed else 1
            obj.save()
        except Exception as e:
            raise SubmissionCreationException(e)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, related_name='user_subscription', on_delete=models.DO_NOTHING)
    track = models.OneToOneField(
        Track, related_name='subscription',
        on_delete=models.DO_NOTHING)
    date_time_created = models.DateTimeField(
        _('Subscription Date and Time'), auto_now_add=True, editable=False)
    date_time_modified = models.DateTimeField(
        _('Subscription Modification Date and Time'), auto_now=True)

    def __str__(self):
        return 'Subscription: {}. Track: {}. User: {}'.format(
            self.id,
            self.track,
            self.user
        )
