import factory

from courses.models import Track
from courses.models import Unit


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track
    
    name = factory.Faker('name')
    description = factory.Faker('name')
    is_published = False
    programming_language = factory.Faker('name')


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit
    
    name = factory.Faker('name')
    description = factory.Faker('name')
    is_published = False
    track = factory.SubFactory('fixtures.factories.courses.TrackFactory')
