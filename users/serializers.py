# users/serializers.py
from rest_framework import serializers
from .models import User


class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)


class EmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

