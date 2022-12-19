from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from .factories import UserFactory


class ApiViewsTests(APITestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory()
        self.client = APIRequestFactory()
    
    # TODO(murat): Add real code to this dummy test
    def test_(self):
        self.assertTrue(True)