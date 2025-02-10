from django.urls import path
from .views import RegisterUserView, LoginUserView, LogoutUserView, RefreshTokenView

app_name = "users"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]

