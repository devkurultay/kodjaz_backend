from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models import Track
from courses.models import Unit
from courses.models import Lesson
from courses.models import Exercise
from courses.models import Submission
from courses.models import Subscription


class PreviousExerciseSerializerField(serializers.Field):
    def to_representation(self, obj):
        prev = Exercise.objects.filter(next_exercise__id=obj.id).first()
        return prev.id if prev else ''

    def to_internal_value(self, data):
        if data:
            prev = Exercise.objects.get(id=data)
        else:
            prev = None
        return { 'previous_exercise': prev }


class ExerciseSerializer(serializers.ModelSerializer):
    entity_type = serializers.SerializerMethodField()
    previous_exercise = PreviousExerciseSerializerField(source='*', required=False)
    default_code = serializers.CharField(trim_whitespace=False, required=False, allow_blank=True)
    unit_test = serializers.CharField(trim_whitespace=False, required=False, allow_blank=True)

    class Meta:
        model = Exercise
        fields = (
            'id', 'name', 'entity_type', 'lecture', 'instruction', 'hint', 'default_code',
            'input_should_contain', 'input_should_not_contain', 'input_error_text',
            'input_should_contain_error_msg', 'input_should_not_contain_error_msg',
            'output_should_contain', 'output_should_not_contain', 'output_error_text',
            'output_should_contain_error_msg', 'output_should_not_contain_error_msg',
            'unit_test', 'previous_exercise', 'next_exercise', 'is_published',
            'lesson', 'unit_id', 'track_id', 'text_file_content'
        )
    
    def get_entity_type(self, obj):
        return Exercise.__name__
    

class UserExerciseSerializer(ExerciseSerializer):
    progress_data = serializers.SerializerMethodField()

    class Meta(ExerciseSerializer.Meta):
        fields = ExerciseSerializer.Meta.fields + ('progress_data',)

    def get_progress_data(self, exercise):
        user = self.context['user']
        return exercise.get_progress_data(user)


class SubmissionSerializer(serializers.ModelSerializer):
    passed = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = Submission
        fields = [
            'id', 'submitted_code', 'exercise', 'passed', 'console_output', 'error_message'
        ]


class LessonSerializer(serializers.ModelSerializer):
    lesson_exercises = ExerciseSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id', 'name', 'entity_type', 'is_published',
            'lesson_exercises', 'unit'
        )
    
    def get_entity_type(self, obj):
        return Lesson.__name__


class UserLessonSerializer(LessonSerializer):
    progress_data = serializers.SerializerMethodField()

    class Meta(LessonSerializer.Meta):
        fields = LessonSerializer.Meta.fields + ('progress_data',)

    def get_progress_data(self, lesson):
        user = self.context['user']
        return lesson.get_progress_data(user)


class UnitSerializer(serializers.ModelSerializer):
    unit_lessons = LessonSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = (
            'id', 'name', 'entity_type', 'description',
            'unit_lessons', 'is_published', 'track'
        )

    def get_entity_type(self, obj):
        return Unit.__name__


class UserUnitSerializer(UnitSerializer):
    progress_data = serializers.SerializerMethodField()

    class Meta(UnitSerializer.Meta):
        fields = UnitSerializer.Meta.fields + ('progress_data',)

    def get_progress_data(self, unit):
        user = self.context['user']
        return unit.get_progress_data(user)


class TrackSerializer(serializers.ModelSerializer):
    track_units = UnitSerializer(many=True, read_only=True)
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = (
            'id', 'name', 'entity_type', 'description',
            'track_units', 'is_published', 'programming_language'
        )

    def get_entity_type(self, obj):
        return Track.__name__


class UserTrackSerializer(TrackSerializer):
    progress_data = serializers.SerializerMethodField()

    class Meta(TrackSerializer.Meta):
        fields = TrackSerializer.Meta.fields + ('progress_data',)

    def get_progress_data(self, track):
        user = self.context['user']
        return track.get_progress_data(user)


class UserSubscriptionSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        track = attrs.get('track')
        user = self.context['user']
        if Subscription.objects.filter(user=user, track=track).exists():
            message = 'The fields user, track must make a unique set.'
            raise ValidationError(message, code='unique')
        return attrs

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'track')
        extra_kwargs = {'user': {'required': False}}
        read_only_fields = ('user', )

    def create(self, validated_data):
        user = self.context['user']
        sub = Subscription.objects.create(user=user, track=validated_data['track'])
        return sub
