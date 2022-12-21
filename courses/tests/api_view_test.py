from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from fixtures.factories.courses import LessonFactory
from fixtures.factories.courses import SubmissionFactory
from fixtures.factories.courses import TrackFactory
from fixtures.factories.courses import UnitFactory
from fixtures.factories.user import UserFactory


class AuthViewsTests(APITestCase):

    def _get_user_client(self, user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def setUp(self):
        super().setUp()
        regular_user = UserFactory()
        admin_user = UserFactory(is_staff=True)
        self.regular_user_client = self._get_user_client(regular_user)
        self.admin_user_client = self._get_user_client(admin_user)

    def test_regular_user_cannot_create_new_tracks(self):
        url = '/api/v1/tracks/'
        data = {
            "name": "Intro to Golang123",
            "description": "Golang is a cool language",
            "is_published": False,
            "programming_language": "Go"
        }
        response = self.regular_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')
    
    def test_admin_user_can_create_new_tracks(self):
        url = '/api/v1/tracks/'
        data = {
            "name": "Intro to Golang123",
            "description": "Golang is a cool language",
            "is_published": False,
            "programming_language": "Go"
        }
        response = self.admin_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_new_units(self):
        url = '/api/v1/units/'
        data = {
            "name": "Some unit",
            "description": "Some awesome unit",
            "is_published": True,
            "track": 0
        }
        response = self.regular_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')

    def test_admin_user_can_create_new_units(self):
        track = TrackFactory()
        url = '/api/v1/units/'
        data = {
            "name": "Some unit",
            "description": "Some awesome unit",
            "is_published": True,
            "track": track.id
        }
        response = self.admin_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_new_lessons(self):
        url = '/api/v1/lessons/'
        data = {
            "name": "Some awesome lesson",
            "is_published": True,
            "unit": 0
        }
        response = self.regular_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')

    def test_admin_user_can_create_new_lessons(self):
        unit = UnitFactory()
        url = '/api/v1/lessons/'
        data = {
            "name": "Some awesome lesson",
            "is_published": True,
            "unit": unit.id
        }
        response = self.admin_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_new_exercises(self):
        lesson = LessonFactory()
        url = '/api/v1/exercises/'
        data = {
            "name": "Hello world",
            "lecture": "print() is used for ...",
            "instruction": "Print out hello world",
            "hint": "Use print()",
            "default_code": "print('hello world')",
            "input_should_contain": "Some test for input inclusion",
            "input_should_not_contain": "Some test for input exclusion",
            "input_error_text": "Error explanation text",
            "output_should_contain": "Some test for output inclusion",
            "output_should_not_contain": "Some test for output exclusion",
            "output_error_text": "Error explanation text",
            "unit_test": "Some code goes here",
            "previous_exercise": "Some prev exercise",
            "next_exercise": 0,
            "is_published": True,
            "lesson": lesson.id,
            "text_file_content": "Some content"
        }
        response = self.regular_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')
    
    def test_admin_user_can_create_new_exercises(self):
        lesson = LessonFactory()
        url = '/api/v1/exercises/'
        data = {
            "name": "Hello world",
            "lecture": "print() is used for ...",
            "instruction": "Print out hello world",
            "hint": "Use print()",
            "default_code": "print('hello world')",
            "input_should_contain": "Some test for input inclusion",
            "input_should_not_contain": "Some test for input exclusion",
            "input_error_text": "Error explanation text",
            "output_should_contain": "Some test for output inclusion",
            "output_should_not_contain": "Some test for output exclusion",
            "output_error_text": "Error explanation text",
            "unit_test": "Some code goes here",
            "is_published": True,
            "lesson": lesson.id,
            "text_file_content": "Some content"
        }
        response = self.admin_user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SumissionTests(APITestCase):

    def setUp(self) -> None:
        self.orig_submission = SubmissionFactory()
        return super().setUp()
    
    def test_submission_permissions(self):
        url = f'/api/v1/submissions/{self.orig_submission.id}/'
        data = {'submitted_code': 'print("Hi!")'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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