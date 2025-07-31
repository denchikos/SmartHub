from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/phone/', views.UnifiedRegisterView.as_view(), name='register_phone'),
    path('register/email/', views.UnifiedRegisterView.as_view(), name='register_email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/google/login/", views.google_login, name="google_login"),
    path("auth/google/callback/", views.google_callback, name="google_callback"),
    path("password/forgot/", views.ForgotPasswordView.as_view(), name="forgotpassword"),
    path('password/reset_page/', views.ResetPasswordPageView.as_view(), name='resetpasswordpage'),
    path('password/reset/', views.ResetPasswordView.as_view(), name='resetpasswordapi'),
]




