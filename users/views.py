from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.http import JsonResponse
import json
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
            return Response({'token': str(refresh.access_token)})
        return Response(serializer.errors, status=400)


def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            password = data.get("password", "").strip()

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Користувач з такою електронною поштою вже існує", "field": "email"},
                                    status=400)

            if User.objects.filter(phone=phone).exists():
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
            return Response({'token': str(refresh.access_token)})
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

            if user and user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)})
            return Response({'error': 'Невірні дані для входу'}, status=400)
        return Response(serializer.errors, status=400)
