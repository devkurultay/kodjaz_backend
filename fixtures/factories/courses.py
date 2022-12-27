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
    input_should_contain = "print,hello"
    input_should_contain_error_msg='Your code should contain {}!'
    input_should_not_contain = "return"
    input_should_not_contain_error_msg = 'Your code should not contain {}!'
    input_error_text = "Error explanation text"
    output_should_contain = "hello"
    output_should_contain_error_msg = "The output should contain {}!"
    output_should_not_contain = "Error"
    output_should_not_contain_error_msg = 'It seems there\'s an error in your output'
    output_error_text = "Error explanation text"
    unit_test = ""
    is_published = False
    lesson = factory.SubFactory('fixtures.factories.courses.LessonFactory')


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission
    
    user = factory.SubFactory('fixtures.factories.user.UserFactory')
    exercise = factory.SubFactory('fixtures.factories.courses.ExerciseFactory')
    submitted_code = "print('hi')"
    passed = True
