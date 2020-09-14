import json

from rest_framework import serializers
import re
import pytz
import datetime
from django.core.validators import ValidationError
from .models import Category, Content 

class VODCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)

class VODContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Content
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)
