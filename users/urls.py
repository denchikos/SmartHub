from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/phone/', views.PhoneRegisterView.as_view(), name='register_phone'),
    path('register/email/', views.EmailRegisterView.as_view(), name='register_email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




