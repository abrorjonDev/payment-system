from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import phone_number_validator

User = get_user_model()



class UserExistsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[phone_number_validator])


class AuthSerializer(serializers.Serializer):
    """For Register and Login"""
    phone_number = serializers.CharField(required=True, validators=[phone_number_validator])
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)


class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[phone_number_validator])
    otp = serializers.IntegerField(write_only=True)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'phone_number2', 'first_name', 'last_name',)
