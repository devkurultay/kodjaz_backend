from rest_framework import serializers

from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'description', 'is_published', 'programming_language']


class UnitSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    class Meta:
        model = Unit
        fields = ['id', 'name', 'description', 'is_published', 'track']


class LessonSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'is_published', 'unit']


class ExerciseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'lecture', 'instruction', 'hint', 'default_code',
            'input_should_contain', 'input_should_not_contain', 'input_error_text',
            'output_should_contain', 'output_should_not_contain', 'output_error_text',
            'unit_test', 'next_exercise', 'is_published', 'lesson', 'text_file_content'
        ]
