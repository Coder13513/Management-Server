import json

from rest_framework import serializers
import re
import pytz
import datetime
from django.core.validators import ValidationError

from radio.models import RadioCategory, RadioChannel


class RadioChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RadioChannel
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)


class RadioCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RadioCategory
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)
