import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ('plaintext_password',)

    email = factory.Faker('email')
    username = factory.Faker('name')
    plaintext_password = factory.PostGenerationMethodCall(
        'set_password', 'defaultpassword'
    )
