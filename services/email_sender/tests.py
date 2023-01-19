from unittest.mock import MagicMock
from unittest.mock import patch
from django.test import SimpleTestCase

from .app import handler


class LambdaFunctionHandlerTests(SimpleTestCase):
    
    @patch('services.email_sender.app.send_email')
    def test_lambda_handler_calls_send_email(self, mock_send_email):
        sender = 'test@example.com'
        recipients = ['recepient@example.com']
        aws_region = 'test-region'
        subject = 'Test subject'
        body_text = 'Body text'
        body_html = '<html></html>'

        email_params = {
            'sender': sender,
            'recipients': recipients,
            'aws_region': aws_region,
            'subject': subject,
            'body_text': body_text,
            'body_html': body_html
        }

        payload = {'email_params': email_params}
        handler(payload, None)
        mock_send_email.assert_called_once_with(**email_params)
    
    @patch('services.email_sender.app.boto3.client')
    def test_(self, mock_client):
        sender = 'test@example.com'
        recipients = ['recepient@example.com']
        aws_region = 'test-region'
        subject = 'Test subject'
        body_text = 'Body text'
        body_html = '<html></html>'

        email_params = {
            'sender': sender,
            'recipients': recipients,
            'aws_region': aws_region,
            'subject': subject,
            'body_text': body_text,
            'body_html': body_html
        }

        payload = {'email_params': email_params}

        expected_success_msg = 'Email sent! Message ID:'
        expected_msg_id = '123'

        # Replace boto3.client.send_email with a mocked one
        send_email_mock = MagicMock()
        send_email_mock.return_value = {'MessageId': expected_msg_id}
        mock_client.return_value = MagicMock(send_email=send_email_mock)

        bfr = []
        def mocked_print(*vals):
            for val in vals:
                bfr.append(val)

        # Replace built-in print with our helper
        with patch('services.email_sender.app.print', mocked_print):

            handler(payload, None)
            self.assertIn(expected_msg_id, bfr)
            self.assertIn(expected_success_msg, bfr)
