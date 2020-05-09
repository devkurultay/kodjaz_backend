from rest_framework import serializers

from courses.models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'description', 'is_published', 'programming_language']

