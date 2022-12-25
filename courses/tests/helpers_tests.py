import json

from unittest.mock import patch
from rest_framework.test import APITestCase
from django.conf import settings

from courses.helpers import run_code
from courses.helpers import is_input_correct


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


class IsInputCorrectTest(APITestCase):

    def test_returns_false_when_code_has_not_all_required_items(self):
        code = 'read = True'
        input_should_contain = 'print,Hello'
        res = is_input_correct(code, input_should_contain, '')
        self.assertFalse(res)
    
    def test_returns_true_when_code_has_all_required_items(self):
        code = 'print("Hello world")'
        input_should_contain = 'print,Hello,world'
        res = is_input_correct(code, input_should_contain, '')
        self.assertTrue(res)

    def test_returns_true_when_should_contain_is_empty(self):
        code = 'print("Hello world")'
        input_should_contain = ''
        res = is_input_correct(code, input_should_contain, '')
        self.assertTrue(res)
    
    def test_false_when_code_has_not_all_required_items(self):
        code = 'print("Hello world")'
        input_should_contain = ''
        res = is_input_correct(code, input_should_contain, '')
        self.assertTrue(res)
    
    def test_returns_false_when_code_contains_unwanted_keywords(self):
        code = "def sum(x,y):\n    print('hi')\nreturn x+y"
        input_should_not_contain = 'print,Hello'
        res = is_input_correct(code, '', input_should_not_contain)
        self.assertFalse(res)
    
    def test_returns_true_when_code_contains_no_unwanted_keywords(self):
        code = "def sum(x,y):\n    return x+y"
        input_should_not_contain = 'print,Hello'
        res = is_input_correct(code, '', input_should_not_contain)
        self.assertTrue(res)