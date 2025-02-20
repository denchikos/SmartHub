from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
from .models import CustomUser
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import LoginUsersForm
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

class LoginUser(LoginView):
    form_class = LoginUsersForm
    template_name = 'users/login_modal.html'
    extra_context = {'title': 'Авторизація'}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    pass


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Привіт, {request.user.username}!"})
