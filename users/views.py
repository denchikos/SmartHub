from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def get_tokens_for_user(user):
    """Генерація JWT-токенів для користувача"""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


class RegisterUserView(APIView):
    """Реєстрація нового користувача"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Користувач з таким логіном вже існує"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        tokens = get_tokens_for_user(user)

        return Response({"message": "Реєстрація успішна", "tokens": tokens}, status=201)


class LoginUserView(APIView):
    """Авторизація користувача"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Неправильний логін або пароль"}, status=400)

        tokens = get_tokens_for_user(user)
        return Response({"message": "Вхід успішний", "tokens": tokens}, status=200)


class LogoutUserView(APIView):
    """Вихід користувача"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вихід успішний"}, status=200)
        except Exception:
            return Response({"error": "Помилка виходу"}, status=400)


class RefreshTokenView(APIView):
    """Оновлення токенів"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({"access": access_token}, status=200)
        except Exception:
            return Response({"error": "Невалідний refresh-токен"}, status=400)
