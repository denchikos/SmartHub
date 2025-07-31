from urllib.parse import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import login
import re
from .serializers import LoginSerializer
from .models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.views import View



def google_login(request):
    """Генерує URL для авторизації через Google та перенаправляє користувача"""
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(settings.GOOGLE_SCOPES),
        "access_type": "offline",
        "prompt": "select_account",  # Щоб користувач міг вибрати акаунт
    }
    auth_url = f"{settings.GOOGLE_AUTH_URI}?{urlencode(params)}"
    print("Google OAuth URL:", auth_url)
    return redirect(auth_url)


def google_callback(request):
    """Обробляє відповідь від Google OAuth і отримує токен"""
    code = request.GET.get("code")

    if not code:
        return redirect("/")  # Якщо немає коду, повертаємо на головну

    # Обмін коду на access_token
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(settings.GOOGLE_TOKEN_URI, data=data)
    token_info = response.json()

    if "access_token" not in token_info:
        return redirect("/")  # Помилка токену

    access_token = token_info["access_token"]

    # Отримання даних користувача
    user_info_response = requests.get(
        settings.GOOGLE_USER_INFO_URI,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user, created = User.objects.get_or_create(email=email, defaults={"is_active": True})
    if created:
        user.set_unusable_password()
        user.save()

    login(request, user)

    # Генерація JWT токена
    refresh = RefreshToken.for_user(user)
    access_token_jwt = str(refresh.access_token)

    # Редірект з токеном у URL
    return redirect(f"/?token={access_token_jwt}")


def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)


def is_valid_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)


class UnifiedRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        password = data.get("password", "").strip()

        # Перевірка формату email / телефону
        if email and not is_valid_email(email):
            return Response({"email": ["Некоректний формат email."]}, status=400)

        if phone and not is_valid_phone(phone):
            return Response({"phone_number": ["Некоректний формат номера телефону."]}, status=400)

        # Перевірка на унікальність
        if email and User.objects.filter(email=email).exists():
            return Response({"email": ["Користувач з такою електронною поштою вже існує."]}, status=400)

        if phone and User.objects.filter(phone=phone).exists():
            return Response({"phone_number": ["Користувач з таким номером телефону вже існує."]}, status=400)

        # Створення користувача
        try:
            user = User.objects.create_user(email=email or None, phone=phone or None, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token),
                "email": user.email,
                "phone": user.phone
            }, status=201)

        except Exception as e:
            return Response({"detail": "Не вдалося створити користувача."}, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data['password']


            try:
                if email:
                    user = User.objects.get(email=email)
                else:
                    user = User.objects.get(phone=phone)

                if not user.check_password(password):
                    return Response({'error': 'Невірний пароль'}, status=400)

                if not user.is_active:
                    return Response({'error': 'Користувач не активний'}, status=400)

                refresh = RefreshToken.for_user(user)
                refresh['pwd_time'] = int(user.password_update_at.timestamp())

                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'success': 'Ви успішно авторизувалися'
                })

            except User.DoesNotExist:
                return Response({'error': 'Користувача не знайдено'}, status=400)

        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Додаємо токен у чорний список
            return Response({"message": "Вихід успішний"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Клас для відсилання листа на пошту
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Користувача з такою поштою не знайдено."}, status=400)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/password/reset_page/?uid={uid}&token={token}"

        send_mail(
            subject="Відновлення пароля",
            message=f"Перейдіть за посиланням для зміни пароля: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"success": "Інструкції надіслано на вашу пошту."})


class ResetPasswordPageView(View):
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        if uid and token:
            return render(request, 'users/reset_password.html', {'uid': uid, 'token': token})


def logout_user_from_deviced(users):
    tokens = OutstandingToken.objects.filter(user=users)

    for token in tokens:
        try:
            BlacklistedToken.objects.get_or_create(token=token)
        except:
            pass


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        print("Отримано POST-запит на скидання пароля")
        print("UID (encoded):", uid)
        print("Token:", token)

        if not uid or not token or not password:
            return Response({"error": "Всі поля обов'язкові."}, status=400)

        try:
            decoded_uid = urlsafe_base64_decode(uid).decode()
            print("UID (decoded):", decoded_uid)
            user = User.objects.get(pk=decoded_uid)
            print("Знайдено користувача:", user)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as e:
            print("Помилка при пошуку користувача:", e)
            return Response({"error": "Недійсне посилання."}, status=400)

        if not default_token_generator.check_token(user, token):
            print("Токен недійсний або протермінований.")
            return Response({"error": "Недійсний або протермінований токен."}, status=400)

        # Встановлюємо новий пароль
        user.set_password(password)
        print("Пароль після set_password:", user.password)
        user.save()
        print("Пароль після save:", user.password)
        logout_user_from_deviced(user)

        return Response({"success": "Пароль успішно змінено."})
