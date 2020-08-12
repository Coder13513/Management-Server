import json

from rest_framework import serializers
import re
import pytz
import datetime
from django.core.validators import ValidationError

from .models import Home


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)
