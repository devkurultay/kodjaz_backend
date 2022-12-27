from django.test import SimpleTestCase

from .app import handler

class LambdaFunctionHandlerTests(SimpleTestCase):
    
    def test_lambda_handler_executes_code_and_returns_output(self):
        sample_code_to_run = "def sum(x,y):\n    return x+y\nprint(sum(3,4))"
        payload = {'answer': sample_code_to_run}
        res = handler(payload, None)
        self.assertEqual(res, '7\n')
    
    def test_shows_exception_name_as_well_as_message(self):
        sample_code_to_run = "def sum(x,y):\n    return x+y\nprint(sum('3',4))"
        expected_output = 'TypeError: can only concatenate str (not "int") to str\n'
        payload = {'answer': sample_code_to_run}
        res = handler(payload, None)
        self.assertEqual(res, expected_output)