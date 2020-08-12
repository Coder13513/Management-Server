import json

from rest_framework import serializers
import re
import pytz
import datetime
from django.core.validators import ValidationError
from archives.models import Archives

class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archives
        fields = ('__all__')
        # exclude = ('deleted',)
    
    def update(self, instance, validated_data):
        instance.save()
        return super().update(instance, validated_data)
