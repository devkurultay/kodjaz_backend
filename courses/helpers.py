import json
import requests

from django.conf import settings


def is_input_correct(submitted_code, should_contain, should_not_contain):
    if should_contain:
        wanted_items = should_contain.split(',')
        for item in wanted_items:
            if item not in submitted_code:
                return False

    if should_not_contain:
        unwanted_items = should_not_contain.split(',')
        for item in unwanted_items:
            if item in submitted_code:
                return False

    return True


def run_code(submitted_code, programming_language):
    msg = '{}: should not be empty'
    if not submitted_code:
        raise ValueError(msg.format('sumitted_code'))
    if not programming_language:
        raise ValueError(msg.format('programming_language'))

    if programming_language.lower() == 'python':
        url = settings.AWS_PYTHON_EXEC_LAMBDA_URL
        headers = {"x-api-key": settings.AWS_API_GATEWAY_API_KEY}
        #TODO(murat): Append unit test code to the submission code
        payload = {'answer': submitted_code}
        res = requests.post(url, json=payload, headers=headers)
        return res.json()
    return 'output'