import json

from unittest.mock import patch
from unittest.mock import MagicMock
from rest_framework.test import APITestCase
from django.conf import settings

from courses.helpers import run_code
from courses.helpers import check_text_source
from courses.helpers import InputObject
from courses.helpers import Checker


class HelpersTests(APITestCase):

    def test_run_code_raises_error_when_submitted_code_is_empty(self):
        with self.assertRaises(ValueError):
            run_code('', 'python')
    
    def test_run_code_raises_error_when_programming_language_is_empty(self):
        with self.assertRaises(ValueError):
            run_code('print("Hi")', '')

    @patch('courses.helpers.requests.post')
    def test_run_code_sends_network_call_to_lambda(self, mock_request_post):
        lang = 'Python'
        code = 'print("Hi!")'
        run_code(code, lang)
        url = settings.AWS_PYTHON_EXEC_LAMBDA_URL
        headers = {'x-api-key': settings.AWS_API_GATEWAY_API_KEY}
        expected_payload = {'answer': code}
        mock_request_post.assert_called_once_with(
            url, json=expected_payload, headers=headers)


class CheckTextSourceTest(APITestCase):

    def test_returns_false_when_code_has_not_all_required_items(self):
        code = 'read = True'
        input_should_contain = 'print,Hello'
        error_msg = 'Oops'
        res = check_text_source(code, input_should_contain, '', error_msg)
        self.assertFalse(res[0])
        self.assertEqual(res[1], error_msg)
    
    def test_returns_true_when_code_has_all_required_items(self):
        code = 'print("Hello world")'
        input_should_contain = 'print,Hello,world'
        res = check_text_source(code, input_should_contain, '', '')
        self.assertTrue(res[0])
        self.assertEqual(res[1], '')

    def test_returns_true_when_should_contain_is_empty(self):
        code = 'print("Hello world")'
        input_should_contain = ''
        res = check_text_source(code, input_should_contain, '', '')
        self.assertTrue(res[0])
        self.assertEqual(res[1], '')
    
    def test_false_when_code_has_not_all_required_items(self):
        code = 'print("Hello world")'
        input_should_contain = ''
        res = check_text_source(code, input_should_contain, '', '')
        self.assertTrue(res[0])
        self.assertEqual(res[1], '')
    
    def test_returns_false_when_code_contains_unwanted_keywords(self):
        code = "def sum(x,y):\n    print('hi')\nreturn x+y"
        input_should_not_contain = 'print,Hello'
        error_msg = 'Your code should not contain print or Hello'
        res = check_text_source(code, '', input_should_not_contain, error_msg)
        self.assertFalse(res[0])
        self.assertEqual(res[1], error_msg)
    
    def test_returns_true_when_code_contains_no_unwanted_keywords(self):
        code = "def sum(x,y):\n    return x+y"
        input_should_not_contain = 'print,Hello'
        res = check_text_source(code, '', input_should_not_contain, '')
        self.assertTrue(res[0])
        self.assertEqual(res[1], '')
    
    def test_can_be_used_to_check_if_output_text_contains_unwanted_keywords(self):
        output_text = "TypeError: can only concatenate str (not \"int\") to str\n"
        input_should_not_contain = 'TypeError'
        error_msg = 'Oops, looks like your code contains some errors'
        res = check_text_source(output_text, '', input_should_not_contain, error_msg)
        self.assertFalse(res[0])
        self.assertEqual(res[1], error_msg)
    
    def test_returns_true_when_source_has_wanted_items_and_has_no_unwanted_ones(self):
        output_text = 'hi!'
        input_should_contain = 'hi!'
        input_should_not_contain = 'TypeError'
        res = check_text_source(
            output_text, input_should_contain, input_should_not_contain, '')
        self.assertTrue(res[0])
        self.assertEqual(res[1], '')


class CheckerTests(APITestCase):

    def test_input_should_not_contain_error_msg_is_returned_when_input_has_no_required_item(self):
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print('hi')",
            unit_test="",
            input_should_contain='sum,return',
            input_should_contain_error_msg='Your code should contain {} keyword',
            input_should_not_contain='',
            input_should_not_contain_error_msg='',
            output_should_contain='',
            output_should_contain_error_msg='',
            output_should_not_contain='',
            output_should_not_contain_error_msg=''
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        self.assertEqual(result['console_output'], '')
        self.assertEqual(
            result['error_msg'],
            input_object.input_should_contain_error_msg.format('return') + '\n')

    def test_input_should_not_contain_error_msg_is_returned_when_input_has_illegal_items(self):
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print('hi')\nreturn x+y",
            unit_test="assert sum(3,3) == 6",
            input_should_contain='return',
            input_should_contain_error_msg='Your code should contain {} keyword',
            input_should_not_contain='print',
            input_should_not_contain_error_msg='Your code should not contain {} keyword',
            output_should_contain='',
            output_should_contain_error_msg='',
            output_should_not_contain='',
            output_should_not_contain_error_msg=''
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        self.assertEqual(result['console_output'], '')
        self.assertEqual(
            result['error_msg'],
            input_object.input_should_not_contain_error_msg.format('print'))
    
    def test_both_input_checks_dont_pass(self):
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print('hi')",
            unit_test="assert sum(3,3) == 6, 'Oops! Your function should return a value!'",
            input_should_contain='return',
            input_should_contain_error_msg='Your code should contain {} keyword',
            input_should_not_contain='print',
            input_should_not_contain_error_msg='Your code should not contain {} keyword',
            output_should_contain='',
            output_should_contain_error_msg='',
            output_should_not_contain='',
            output_should_not_contain_error_msg=''
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        self.assertEqual(result['console_output'], '')
        expected_err_msg = (
            input_object.input_should_contain_error_msg.format('return') + '\n' +
            input_object.input_should_not_contain_error_msg.format('print')
        )
        self.assertEqual(
            result['error_msg'],
            expected_err_msg)
    
    @patch('courses.helpers.requests.post')
    def test_output_should_contain_error_msg_is_returned_when_output_has_no_required_item(
            self, mock_request):
        expected_output = ''
        mock_response = MagicMock()
        mock_response.json.return_value = expected_output
        mock_request.return_value = mock_response
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    return x+y",
            unit_test="sum(3,3)",
            input_should_contain='',
            input_should_contain_error_msg='',
            input_should_not_contain='',
            input_should_not_contain_error_msg='',
            output_should_contain='6',
            output_should_contain_error_msg='Your output should contain {}. But it doesn\'t.',
            output_should_not_contain='',
            output_should_not_contain_error_msg=''
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        self.assertEqual(result['console_output'], '')
        self.assertEqual(
            result['error_msg'],
            input_object.output_should_contain_error_msg.format('6') + '\n')
    
    @patch('courses.helpers.requests.post')
    def test_output_should_not_contain_error_msg_is_returned_when_output_has_illegal_items(
            self, mock_request):
        expected_output = 'hi\n'
        mock_response = MagicMock()
        mock_response.json.return_value = expected_output
        mock_request.return_value = mock_response
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print('hi')",
            unit_test="sum(3,3)",
            input_should_contain='',
            input_should_contain_error_msg='',
            input_should_not_contain='',
            input_should_not_contain_error_msg='',
            output_should_contain='',
            output_should_contain_error_msg='',
            output_should_not_contain='hi',
            output_should_not_contain_error_msg='You should have removed "{}". But it looks like you haven\'t'
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        self.assertEqual(
            result['error_msg'],
            input_object.output_should_not_contain_error_msg.format('hi'))
    
    @patch('courses.helpers.requests.post')
    def test_bot_output_checks_fail(self, mock_request):
        expected_output = 'hi\n'
        mock_response = MagicMock()
        mock_response.json.return_value = expected_output
        mock_request.return_value = mock_response
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print('hi')",
            unit_test="sum(3,3)",
            input_should_contain='',
            input_should_contain_error_msg='',
            input_should_not_contain='',
            input_should_not_contain_error_msg='',
            output_should_contain='6',
            output_should_contain_error_msg='Your code should return "{}", but it does not',
            output_should_not_contain='hi',
            output_should_not_contain_error_msg='You should have removed "{}". But it looks like you haven\'t'
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertFalse(result['success'])
        expected_error_msg = (
            input_object.output_should_contain_error_msg.format('6') + '\n' +
            input_object.output_should_not_contain_error_msg.format('hi')
        )
        self.assertEqual(result['console_output'], expected_output)
        self.assertEqual(result['error_msg'], expected_error_msg)

    @patch('courses.helpers.requests.post')
    def test_happy_case_empty_match_checks(self, mock_request):
        expected_output = '6\n'
        mock_response = MagicMock()
        mock_response.json.return_value = expected_output
        mock_request.return_value = mock_response
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print(3+3)",
            unit_test="sum(3,3)",
            input_should_contain='',
            input_should_contain_error_msg='',
            input_should_not_contain='',
            input_should_not_contain_error_msg='',
            output_should_contain='',
            output_should_contain_error_msg='',
            output_should_not_contain='hi',
            output_should_not_contain_error_msg=''
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertTrue(result['success'])
        self.assertEqual(result['console_output'], '6\n')
        self.assertEqual(result['error_msg'], '')
    
    @patch('courses.helpers.requests.post')
    def test_happy_case_all_checks_pass(self, mock_request):
        expected_output = '6\n'
        mock_response = MagicMock()
        mock_response.json.return_value = expected_output
        mock_request.return_value = mock_response
        input_object = InputObject(
            programming_language='Python',
            code="def sum(x,y):\n    print(3+3)",
            unit_test="sum(3,3)",
            input_should_contain='print',
            input_should_contain_error_msg='Your code should contain {}. But it does not',
            input_should_not_contain='return',
            input_should_not_contain_error_msg='Your code should not contain {}. But it does',
            output_should_contain=expected_output,
            output_should_contain_error_msg='The output should contain {}. But it does not',
            output_should_not_contain='hi',
            output_should_not_contain_error_msg='The output should not contain {}. But it contains'
        )
        checker = Checker(input_object)
        result = checker.check()
        self.assertTrue(result['success'])
        self.assertEqual(result['console_output'], '6\n')
        self.assertEqual(result['error_msg'], '')
    
    def test_raises_exception_when_unsupported_language_is_passed(self):
        not_supported_language = 'Python124'
        input_object = InputObject(
            programming_language=not_supported_language,
            code="def sum(x,y):\n    print(3+3)",
            unit_test="sum(3,3)",
            input_should_contain='print',
            input_should_contain_error_msg='Your code should contain {}. But it does not',
            input_should_not_contain='return',
            input_should_not_contain_error_msg='Your code should not contain {}. But it does',
            output_should_contain='6\n',
            output_should_contain_error_msg='The output should contain {}. But it does not',
            output_should_not_contain='hi',
            output_should_not_contain_error_msg='The output should not contain {}. But it contains'
        )
        checker = Checker(input_object)
        with self.assertRaisesMessage(NotImplementedError, f'{not_supported_language} is not supported'):
            checker.check()
