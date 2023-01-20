import json

from unittest.mock import MagicMock
from unittest.mock import patch

from django.core import mail
from django.conf import settings
from django.test import override_settings
from django.test import SimpleTestCase


@override_settings(
    EMAIL_BACKEND = 'authentication.helpers.AWSLambdaSESEmailBackend',
    AWS_S3_REGION_NAME = 'eu-central-1'
)


class AWSLambdaSESEmailBackendTest(SimpleTestCase):

    # @patch('authentication.helpers.AWSLambdaSESEmailBackend.send_messages')
    @patch('authentication.helpers.boto3.client')
    def test_boto3_client_invoke_called(self, mock_client):
        mock_invoke = MagicMock()
        mock_client.return_value = MagicMock(invoke=mock_invoke)

        subject = "Subject"
        message = "Content"
        from_email = 'murat@example.com'
        recipients = ["joe@example.com", "jane@example.com"]
        mail.send_mail(subject, message, from_email, recipients)

        mock_client.assert_called_with('lambda')

        # TODO(murat): set a valid HTML template here or use Django's templates framework
        body_html = '<html></html>'

        expected_email_params = {
            'sender': from_email,
            'recipients': recipients,
            'aws_region': settings.AWS_S3_REGION_NAME,
            'subject': subject,
            'body_text': message,
            'body_html': body_html
        }
        payload_str = json.dumps({'email_params': expected_email_params})
        payload_bytes_arr = bytes(payload_str, encoding='utf8')

        mock_invoke.assert_called_with(
            FunctionName='email_sender',
            InvocationType='Event',
            Payload=payload_bytes_arr
        )
