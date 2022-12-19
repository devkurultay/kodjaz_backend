from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    email = 'admin@admin.admin'
    password = '123'