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
    except:
        return False
    # Return stdout
    sys.stdout = sys.stdout
    return buffer.getvalue()