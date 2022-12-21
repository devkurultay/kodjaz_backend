from rest_framework.test import APITestCase


from courses.helpers import run_code

class HelpersTests(APITestCase):

    def test_run_code_raises_error_when_submitted_code_is_empty(self):
        with self.assertRaises(ValueError):
            run_code('', 'python')
    
    def test_run_code_raises_error_when_programming_language_is_empty(self):
        with self.assertRaises(ValueError):
            run_code('print("Hi")', '')