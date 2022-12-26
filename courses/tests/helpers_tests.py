import json

from unittest.mock import patch
from rest_framework.test import APITestCase
from django.conf import settings

from courses.helpers import run_code
from courses.helpers import check_text_source


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
