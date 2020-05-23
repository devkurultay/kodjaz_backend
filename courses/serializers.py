from rest_framework import serializers

from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'entity_type', 'lecture', 'instruction', 'hint', 'default_code',
            'input_should_contain', 'input_should_not_contain', 'input_error_text',
            'output_should_contain', 'output_should_not_contain', 'output_error_text',
            'unit_test', 'next_exercise', 'is_published', 'lesson', 'text_file_content'
        ]
    
    def get_entity_type(self, obj):
        return Exercise.__name__


class LessonSerializer(serializers.ModelSerializer):
    lesson_exercises = ExerciseSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'entity_type', 'is_published',
            'lesson_exercises', 'unit'
        ]
    
    def get_entity_type(self, obj):
        return Lesson.__name__


class UnitSerializer(serializers.ModelSerializer):
    unit_lessons = LessonSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            'id', 'name', 'entity_type', 'description',
            'unit_lessons', 'is_published', 'track'
        ]

    def get_entity_type(self, obj):
        return Unit.__name__


class TrackSerializer(serializers.ModelSerializer):
    track_units = UnitSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id', 'name', 'entity_type', 'description',
            'track_units', 'is_published', 'programming_language'
        ]

    def get_entity_type(self, obj):
        return Track.__name__
