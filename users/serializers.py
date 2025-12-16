# users/serializers.py
from rest_framework import serializers

class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)


class EmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Перевіряємо, що хоча б одне з полів (email або phone) заповнене"""
        if not data.get("phone") and not data.get("email"):
            raise serializers.ValidationError("Необхідно вказати або email, або телефон.")
        if not data.get("password"):
            raise serializers.ValidationError("Необхідно вказати пароль.")
        return data

