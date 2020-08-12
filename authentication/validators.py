import re
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


def validate_phone_number(phone):
    """Validate the phone number to match expected format"""
    p = re.compile(r'\+?\d{3}\s?\d{3}\s?\d{7}')
    q = re.compile(r'^.{10,16}$')
    if not (p.match(phone) and q.match(phone)):
        raise serializers.ValidationError(
            "Phone number must be of the format +234 123 4567890"
        )

def validate_address(address):
    if not isinstance(address, dict):
        raise ValidationError(
            "Address should contain City, State and Street.")
    KEYS = ["City", "State", "Street"]
    for key in KEYS:
        if key not in address.keys():
            raise ValidationError(
                f"Please provide a {key} name in your address.")
    for key, value in address.items():
        if not isinstance(value, str):
            raise ValidationError(f"{key} should be letters.")
        if not value.strip():
            raise ValidationError(f"{key} cannot be empty!")
