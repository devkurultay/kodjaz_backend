from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.data = {'email': 'test_email@gmail.com',
                     'password': 'test123456',
                     'password2': 'test123456'}
        self.url = reverse('authentication:user_registration')

    def test_user_create_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data['email'], response.data['email'])

    def test_user_passwords_do_not_match(self):
        self.data['password2'] = ''
        response = self.client.post(self.url, self.data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_for_unique_email(self):
        User.objects.create(email='test_email@gmail.com')
        response = self.client.post(self.url, self.data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_validate_email(self):
        self.data['email'] = '12345'
        response = self.client.post(self.url, self.data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_validate_password(self):
        self.data['password'] = '123'
        self.data['password2'] = '123'
        response = self.client.post(self.url, self.data)
        self.assertTrue(status.is_client_error(response.status_code))
