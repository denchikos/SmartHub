# users/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Користувач з таким номером телефону вже існує.")
        return value


class EmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувач з такою електронною поштою вже існує.")
        return value


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data.get("phone") and not data.get("email"):
            raise serializers.ValidationError("Вкажіть або email, або номер телефону.")
        if not data.get("password"):
            raise serializers.ValidationError("Необхідно ввести пароль.")
        return data

