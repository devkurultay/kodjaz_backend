import requests

from django.conf import settings

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
