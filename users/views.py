# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
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
