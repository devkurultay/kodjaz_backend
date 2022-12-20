from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from fixtures.factories.courses import SubmissionFactory
from fixtures.factories.user import UserFactory


class SumissionTests(APITestCase):

    def setUp(self) -> None:
        self.orig_submission = SubmissionFactory()
        return super().setUp()
    
    def test_submission_permissions(self):
        second_user = UserFactory()
        refresh = RefreshToken.for_user(second_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = f'/api/v1/submissions/{self.orig_submission.id}/'
        data = {'submitted_code': 'print("Hi!")'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.')
        
        orig_user = self.orig_submission.user
        refresh = RefreshToken.for_user(orig_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)