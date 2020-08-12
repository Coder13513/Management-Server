from django.urls import path

from authentication.views import (
    RegistrationAPIView, LoginAPIv2View, ProfileView, LogoutAPIView, ValidateOTPAPIView, VerifyAccountAPIView,
    RegistrationAPIv2View
)

app_name = 'authenticationv2'

urlpatterns = [
    path("subscription/", RegistrationAPIView.as_view(), name="subscription"),
    path("register/", RegistrationAPIv2View.as_view(), name="register"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginAPIv2View.as_view(), name="loginv2"),
    path("login/otp/", ValidateOTPAPIView.as_view(), name="otp_validater"),
    path("verify/", VerifyAccountAPIView.as_view(), name="verify_account")
]
