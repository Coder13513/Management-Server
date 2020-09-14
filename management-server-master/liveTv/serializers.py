import json

from rest_framework import serializers
import re
import pytz
import datetime
from django.core.validators import ValidationError

from liveTv.models import Categories, Channels

# from property.validators import (
#     validate_address, validate_coordinates, validate_image_list, validate_visit_date)

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('__all__')
        # exclude = ('deleted',)
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)


class ChannelsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Channels
        fields = ('__all__')
        # exclude = ('deleted',)
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)
