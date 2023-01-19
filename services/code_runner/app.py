import sys
from io import StringIO


def handler(event, context):
    # Get code from payload
    code = event['answer']
    # Capture stdout
    buffer = StringIO()
    sys.stdout = buffer
    # Execute code
    try:
        exec(code)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
    # Return stdout
    sys.stdout = sys.stdout
    return buffer.getvalue()