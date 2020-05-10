from rest_framework import serializers

from courses.models import Track
from courses.models import Unit


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'description', 'is_published', 'programming_language']


class UnitSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    class Meta:
        model = Unit
        fields = ['id', 'name', 'description', 'is_published', 'track']

