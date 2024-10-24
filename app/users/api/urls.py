from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    RegisterView,
    UserExistsView,
    UserView,
    VerifyOtpView,
)

app_name = "api"


urlpatterns = [
    path("exists", UserExistsView.as_view(), name="user_exists"),
    path("register", RegisterView.as_view(), name="register"),
    path("verify", VerifyOtpView.as_view(), name="verify_otp"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("password-change", PasswordChangeView.as_view(), name="password_change"),

    path("user/me", UserView.as_view(), name="user"),
]
