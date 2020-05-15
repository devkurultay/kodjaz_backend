from rest_framework import serializers

from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'lecture', 'instruction', 'hint', 'default_code',
            'input_should_contain', 'input_should_not_contain', 'input_error_text',
            'output_should_contain', 'output_should_not_contain', 'output_error_text',
            'unit_test', 'next_exercise', 'is_published', 'lesson', 'text_file_content'
        ]


class LessonSerializer(serializers.ModelSerializer):
    lesson_exercises = ExerciseSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'is_published', 'lesson_exercises', 'unit']


class UnitSerializer(serializers.ModelSerializer):
    unit_lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ['id', 'name', 'description', 'unit_lessons', 'is_published', 'track']


class TrackSerializer(serializers.ModelSerializer):
    track_units = UnitSerializer(many=True, read_only=True)
    class Meta:
        model = Track
        fields = ['id', 'name', 'description', 'track_units', 'is_published', 'programming_language']
