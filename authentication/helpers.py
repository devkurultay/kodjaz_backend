import json
import boto3

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class AWSLambdaSESEmailBackend(BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently
        self.client = boto3.client('lambda')
        self.aws_region = settings.AWS_S3_REGION_NAME

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        cnt = 0
        for message in email_messages:
            self._send_ses_email_via_lambda(message)
            cnt += 1
        return cnt

    def _send_ses_email_via_lambda(self, email_message):
        # TODO(murat): set a valid HTML template here
        body_html = '<html></html>'
        email_params = {
            'sender': email_message.from_email,
            'recipients': email_message.to,
            'aws_region': self.aws_region,
            'subject': email_message.subject,
            'body_text': email_message.body,
            'body_html': body_html
        }
        payload_str = json.dumps({'email_params': email_params})
        payload_bytes_arr = bytes(payload_str, encoding='utf8')

        self.client.invoke(
            FunctionName='email_sender',
            InvocationType='Event',
            Payload=payload_bytes_arr
        )
