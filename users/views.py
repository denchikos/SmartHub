from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.http import JsonResponse
import json
import re
from .serializers import PhoneRegisterSerializer, EmailRegisterSerializer, LoginSerializer
from .models import User


class PhoneRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = User.objects.create_user(phone=phone, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token), 'phone': user.phone})
        return Response(serializer.errors, status=400)



"""Перевіряє, чи є рядок email-адресою"""
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)


"""Перевіряє, чи є рядок коректним номером телефону (мінімум 10 цифр)"""
def is_valid_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)


def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            password = data.get("password", "").strip()

            if email and not is_valid_email(email):
                return JsonResponse({"error": "Некоректний формат email", "field": "email"}, status=400)

            if phone and not is_valid_phone(phone):
                return JsonResponse({"error": "Некоректний номер телефону", "field": "phone"}, status=400)

            if email and User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Користувач з такою електронною поштою вже існує", "field": "email"},
                                    status=400)

            if phone and User.objects.filter(phone=phone).exists():
                return JsonResponse({"error": "Користувач з таким номером телефону вже існує", "field": "phone"},
                                    status=400)

            user = User.objects.create_user(email=email, phone=phone, password=password)
            return JsonResponse({"success": "Реєстрація успішна"}, status=201)

        except IntegrityError:
            return JsonResponse({"error": "Помилка бази даних. Можливо, такий користувач вже існує"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Невірний формат запиту"}, status=400)

    return JsonResponse({"error": "Метод не дозволено"}, status=405)


class EmailRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create_user(email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token), 'email': user.email})
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = None
            if serializer.validated_data.get('phone'):
                user = User.objects.filter(phone=serializer.validated_data['phone']).first()
            elif serializer.validated_data.get('email'):
                user = User.objects.filter(email=serializer.validated_data['email']).first()

            if not user:
                return Response({'error': 'Користувача не знайдено'}, status=404)

            if not user.check_password(serializer.validated_data['password']):
                return Response({'error': 'Невірний пароль'}, status=400)

            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'success': 'Ви успішно авторизувалися'
            })

        return Response(serializer.errors, status=400)