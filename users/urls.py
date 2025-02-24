from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register_phone_func'),
    path('register/phone/', views.PhoneRegisterView.as_view(), name='register_phone'),
    path('register/email/', views.EmailRegisterView.as_view(), name='register_email'),
    path('login/phone/', views.LoginView.as_view(), name='login_phone'),
    path('login/email/', views.LoginView.as_view(), name='login_email'),
]




