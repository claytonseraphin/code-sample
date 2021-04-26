from rest_framework import serializers
from .models import Survey


class SurveySerializer(serializers.ModelSerializer):
    """Serializer for Survey object."""
    class Meta:
        model = Survey
        fields = ('id', 'first_name', 'last_name', 'is_us_citizen',
                  'is_registered_to_vote')
        read_only_Fields = ('id')


class SurveyImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to survey."""
    class Meta:
        model = Survey
        fields = ('id', 'image')
        read_only_Fields = ('id')
