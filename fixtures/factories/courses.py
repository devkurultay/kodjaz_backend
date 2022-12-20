import factory

from courses.models import Track


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track
    
    name = factory.Faker('name')
    description = factory.Faker('name')
    is_published = False
    programming_language = factory.Faker('name')
