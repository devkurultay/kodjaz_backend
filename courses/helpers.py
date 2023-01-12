import requests

from django.conf import settings
from django.db.models import BooleanField
from django.db.models import Count
from django.db.models import Q
from django.db.models import F
from django.db.models import Exists
from django.db.models import ExpressionWrapper
from django.db.models import OuterRef
from django.db.models.functions import Coalesce
from django.db.models.lookups import GreaterThan
from django.db.models.lookups import Exact

from courses.models import Exercise


def run_code(submitted_code, programming_language):
    msg = '{}: should not be empty'
    if not submitted_code:
        raise ValueError(msg.format('sumitted_code'))
    if not programming_language:
        raise ValueError(msg.format('programming_language'))

    if programming_language.lower() == 'python':
        url = settings.AWS_PYTHON_EXEC_LAMBDA_URL
        headers = {"x-api-key": settings.AWS_API_GATEWAY_API_KEY}
        payload = {'answer': submitted_code}
        res = requests.post(url, json=payload, headers=headers)
        return res.json()
    raise NotImplementedError(f'{programming_language} is not supported')


class CheckInputObject:
    def __init__(
        self,
        programming_language,
        code,
        unit_test,
        input_should_contain,
        input_should_contain_error_msg,
        input_should_not_contain,
        input_should_not_contain_error_msg,
        output_should_contain,
        output_should_contain_error_msg,
        output_should_not_contain,
        output_should_not_contain_error_msg
    ) -> None:
        self.programming_language = programming_language
        self.code = code
        self.unit_test = unit_test
        self.input_should_contain = input_should_contain
        self.input_should_contain_error_msg = input_should_contain_error_msg
        self.input_should_not_contain = input_should_not_contain
        self.input_should_not_contain_error_msg = input_should_not_contain_error_msg
        self.output_should_contain = output_should_contain
        self.output_should_contain_error_msg = output_should_contain_error_msg
        self.output_should_not_contain = output_should_not_contain
        self.output_should_not_contain_error_msg = output_should_not_contain_error_msg


def build_input_object(exercise: Exercise, submitted_code: str) -> CheckInputObject:
    return CheckInputObject(
        programming_language=exercise.lesson.unit.track.programming_language,
        code=submitted_code,
        unit_test=exercise.unit_test,
        input_should_contain=exercise.input_should_contain,
        input_should_contain_error_msg=exercise.input_should_contain_error_msg,
        input_should_not_contain=exercise.input_should_not_contain,
        input_should_not_contain_error_msg=exercise.input_should_not_contain_error_msg,
        output_should_contain=exercise.output_should_contain,
        output_should_contain_error_msg=exercise.output_should_contain_error_msg,
        output_should_not_contain=exercise.output_should_not_contain,
        output_should_not_contain_error_msg=exercise.output_should_not_contain_error_msg
    )


class Checker:
    def __init__(self, inp_obj: CheckInputObject) -> None:
        self.programming_language = inp_obj.programming_language
        self.code = inp_obj.code
        self.unit_test = inp_obj.unit_test

        self.inp_should_contain = inp_obj.input_should_contain
        self.inp_should_contain_error_msg = inp_obj.input_should_contain_error_msg

        self.inp_should_not_contain = inp_obj.input_should_not_contain
        self.inp_should_not_contain_error_msg = inp_obj.input_should_not_contain_error_msg

        self.out_should_contain = inp_obj.output_should_contain
        self.out_should_contain_error_msg = inp_obj.output_should_contain_error_msg

        self.out_should_not_contain = inp_obj.output_should_not_contain
        self.out_should_not_contain_error_msg = inp_obj.output_should_not_contain_error_msg

    def _check_source_contains(self, source, should_contain, should_contain_error_msg):
        if should_contain:
            wanted_items = should_contain.split(',')
            for item in wanted_items:
                if item not in source:
                    return False, should_contain_error_msg.format(item)
        return True, ''
    
    def _check_source_does_not_contain(self, source, should_not_contain, should_not_contain_error_msg):
        if should_not_contain:
            unwanted_items = should_not_contain.split(',')
            for item in unwanted_items:
                if item in source:
                    return False, should_not_contain_error_msg.format(item)
        return True, ''

    def _check_input_contains(self):
        return self._check_source_contains(
            self.code, self.inp_should_contain, self.inp_should_contain_error_msg)

    def _check_input_does_not_contain(self):
        return self._check_source_does_not_contain(
            self.code, self.inp_should_not_contain, self.inp_should_not_contain_error_msg)

    def _run_code(self):
        code_to_run = self.code + '\n' + (self.unit_test if self.unit_test else '')
        return run_code(code_to_run, self.programming_language)

    def _output_contains(self, output):
        return self._check_source_contains(
            output, self.out_should_contain, self.out_should_contain_error_msg)

    def _output_does_not_contain(self, output):
        return self._check_source_does_not_contain(
            output, self.out_should_not_contain, self.out_should_not_contain_error_msg)
    
    def _build_output(self, success, console_output, error_msg):
        # TODO(murat): Return an OutputObject
        return {
            'success': success,
            'console_output': console_output,
            'error_msg': error_msg
        }

    def check(self):
        is_cont_ok, inp_cont_er_msg = self._check_input_contains()
        is_not_cont_ok, inp_not_cont_er_msg = self._check_input_does_not_contain()
        if not is_cont_ok or not is_not_cont_ok:
            error_msg = ''
            error_msg += inp_cont_er_msg + '\n' if not is_cont_ok else ''
            error_msg += inp_not_cont_er_msg if not is_not_cont_ok else ''
            return self._build_output(False, '', error_msg)

        output = self._run_code()
        is_out_cont_ok, out_cont_er_msg = self._output_contains(output)
        is_out_not_cont_ok, out_not_cont_er_msg = self._output_does_not_contain(output)
        if not is_out_cont_ok or not is_out_not_cont_ok:
            error_msg = ''
            error_msg += out_cont_er_msg + '\n' if not is_out_cont_ok else ''
            error_msg += out_not_cont_er_msg if not is_out_not_cont_ok else ''
            return self._build_output(False, output, error_msg)
        
        # All checks passed
        return self._build_output(True, output, '')


# Don't repeat yourself
def get_progress_data(user, entity, instance, filter_key):
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
    in_progress = ExpressionWrapper(in_progress_exp, output_field=BooleanField())

    submissions_sum = F('passed_submissions_count') + F('not_passed_submissions_count')

    filter_kwargs = {filter_key: OuterRef('pk')}
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
    ).filter(**filter_kwargs)

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

    item = entity.objects.annotate(
        is_complete=~Exists(exercise_template_subq.filter(complete_expr)) # NOT EXISTS
    ).annotate(
        is_in_progress=in_progress_expr
    ).get(id=instance.id)
    return {'is_complete': item.is_complete, 'is_in_progress': item.is_in_progress}
