import factory

from courses.models import Lesson
from courses.models import Exercise
from courses.models import Track
from courses.models import Unit
from courses.models import Submission


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track
    
    name = factory.Faker('name')
    description = factory.Faker('name')
    is_published = False
    programming_language = 'Python'


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit
    
    name = factory.Faker('name')
    description = factory.Faker('name')
    is_published = False
    track = factory.SubFactory('fixtures.factories.courses.TrackFactory')


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson
    name = factory.Faker('name')
    is_published = False
    unit = factory.SubFactory('fixtures.factories.courses.UnitFactory')


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    name = factory.Faker('name')
    lecture = factory.Faker('name')
    instruction = "Print out hello world"
    default_code = "print('hello world')"
    input_should_contain = "Some test for input inclusion"
    input_should_not_contain = "Some test for input exclusion"
    input_error_text = "Error explanation text"
    output_should_contain = "Some test for output inclusion"
    output_should_not_contain = "Some test for output exclusion"
    output_error_text = "Error explanation text"
    unit_test = "Some code goes here"
    is_published = False
    lesson = factory.SubFactory('fixtures.factories.courses.LessonFactory')


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission
    
    user = factory.SubFactory('fixtures.factories.user.UserFactory')
    exercise = factory.SubFactory('fixtures.factories.courses.ExerciseFactory')
    submitted_code = "Some code goes here"