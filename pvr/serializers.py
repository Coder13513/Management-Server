import json
from rest_framework import serializers
from authentication.models import User, UserProfile
from pvr.models import Recording
# from property.validators import (
#     validate_address, validate_coordinates, validate_image_list, validate_visit_date)

class RecordingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recording
        fields = ('__all__')

    def create(self, validated_data):
        return Recording.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)

    def availableRecordingTime(self, instance, validated_data):
            print(instance)
