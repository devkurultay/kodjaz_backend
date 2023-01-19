from unittest.mock import MagicMock
from unittest.mock import patch

from django.core import mail
from django.test import override_settings
from django.test import SimpleTestCase


@override_settings(
    EMAIL_BACKEND = 'authentication.helpers.AWSLambdaSESEmailBackend',
    AWS_S3_REGION_NAME = 'eu-central-1'
)


class SendTestEmailManagementCommand(SimpleTestCase):

    @patch('authentication.helpers.AWSLambdaSESEmailBackend.send_messages')
    def test_boto_client_is_called_and_invoked(self, mock_send_msgs):
        recipients = ["joe@example.com", "jane@example.com"]
        subj = "Subject"
        message = "Content"
        from_email = 'murat@example.com'

        mail.send_mail(subj, message, from_email, recipients)

        # EMAIL_BACKEND is set to our custom backend, that's why it's method is called
        mock_send_msgs.assert_called_once()
