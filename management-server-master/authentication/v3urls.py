from django.urls import path

from authentication.v3views import (
    RegistrationAPIView, LoginAPIView, ProfileView, LogoutAPIView, ValidateOTPAPIView, VerifyAccountAPIView,
)

app_name = 'authenticationv3'

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/otp/", ValidateOTPAPIView.as_view(), name="otp_validater"),
    path("verify/", VerifyAccountAPIView.as_view(), name="verify_account")
]
