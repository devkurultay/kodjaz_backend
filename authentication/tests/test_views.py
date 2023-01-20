from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class RegistrationEndpointTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.data = {'email': 'test_email@gmail.com',
                     'password1': 'test123456',
                     'password2': 'test123456'}
        self.url = reverse('authentication:rest_register')

    def test_user_create_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['detail'], 'Verification e-mail sent.')

    def test_user_passwords_do_not_match(self):
        self.data['password2'] = ''
        response = self.client.post(self.url, self.data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_for_unique_email(self):
        User.objects.create(email='test_email@gmail.com')
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.json(),
            {'email': ['A user is already registered with this e-mail address.']}
        )
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_validate_email(self):
        self.data['email'] = '12345'
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.json(),
            {'email': ['Enter a valid email address.']}
        )
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_validate_password(self):
        self.data['password1'] = '123'
        self.data['password2'] = '123'
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.json(),
            {
                'password1': [
                    'This password is too short. It must contain at least 8 characters.',
                    'This password is too common.', 'This password is entirely numeric.'
                ]
            }
        )
        self.assertTrue(status.is_client_error(response.status_code))
