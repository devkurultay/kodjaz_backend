

def run_code(submitted_code, programming_language):
    msg = '{}: should not be empty'
    if not submitted_code:
        raise ValueError(msg.format('sumitted_code'))
    if not programming_language:
        raise ValueError(msg.format('programming_language'))
    # TODO(murat): populate with actual AWS Lambda function invocation code
    return 'output'