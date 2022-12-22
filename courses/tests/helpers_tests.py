import json

from unittest.mock import patch
from rest_framework.test import APITestCase
from django.conf import settings

from courses.helpers import run_code


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
