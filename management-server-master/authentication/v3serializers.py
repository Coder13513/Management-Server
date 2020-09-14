from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.models import (
    User, BlackList, UserProfile, UserDevices
)

from utils.password_generator import randomStringwithDigitsAndSymbols
from utils import BaseUtils
from authentication.validators import validate_phone_number, validate_address
from subscription.manager import SubscriptionSessionManager

class RegistrationSerializer(serializers.ModelSerializer):
    """Serialize registration requests and create a new user."""

    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # role = serializers.ChoiceField(
    #     choices=[('CA', 'client_admin'),('VI', 'viewer')]
    # )

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ["email","password", "confirmed_password"]

    def validate(self,data):

        confirmed_password = data.get("confirmed_password")
        try:
            validate_password(data["password"])
        except ValidationError as identifier:
            raise serializers.ValidationError({
            "password": str(identifier).replace("["", ""]", "")
        })

        if not self.do_passwords_match(data["password"], confirmed_password):
            raise serializers.ValidationError({
                "passwords": ("Passwords do not match")
        })

        return data


    def create(self, validated_data):
        """ create user """
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        """Check if passwords match."""
        return password1 == password2

class LoginSerializer(serializers.Serializer):

    email=serializers.EmailField()
    password=serializers.CharField(
        max_length=128, min_length=6, write_only=True, )
    device_type = serializers.CharField(write_only=True)
    token=serializers.CharField(read_only=True)
    session_manager = SubscriptionSessionManager()

    def validate(self, data):
        email=data.get("email", None),
        password=data.get("password", None)
        device_type=data.get("device_type", None)
        user=authenticate(username=email[0], password=password)
        if user is None:
            raise serializers.ValidationError({
                "invalid": "invalid email and password combination"
            })
        print(device_type)
        session_allowed = self.session_manager.check(user.id, device_type)
        if session_allowed != True:
            raise serializers.ValidationError({
                "user": "User session already active on other devices or User don't have a active subscription"
            })
        if not user.is_verified:
            raise serializers.ValidationError({
                "user": "Your email is not verified, please vist your mail box"
            })
        user={
            "email": user
        }
        return user


class ProfileSerializer(serializers.ModelSerializer, BaseUtils):
    """Serializer to serialize the user profile data"""
    user = RegistrationSerializer()
    address = serializers.JSONField(validators=[validate_address])
    phone = serializers.CharField(
        validators=[validate_phone_number])

    class Meta:
        model = UserProfile
        exclude = ('deleted',)
        read_only_fields = ('user', 'updated_at', 'created_at',
                            'user_level')

        extra_kwargs = {
            'security_question': {'write_only': True},
            'security_answer': {'write_only': True}
        }

    def update(self, instance, validated_data):
        """Update the user profile"""
        instance.save()
        return super().update(instance)

    def validate(self, data):
        """Validate user updated fields"""

        # validate fields that depend on each other
        self.validate_dependent_fields(data,
                                       'security_question',
                                       'security_answer',
                                       'Please provide an answer'
                                       ' to the selected question',
                                       'Please choose a question to answer')

        return data

class BlackListSerializer(serializers.ModelSerializer):
    """
    Handle serializing and deserializing blacklist tokens
    """

    class Meta:
        model=BlackList
        fields=('__all__')
