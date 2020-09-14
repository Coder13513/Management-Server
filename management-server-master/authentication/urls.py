from django.urls import path

from authentication.views import (
    RegistrationAPIView, LoginAPIView, ProfileView, LogoutAPIView
)

app_name = 'authentication'


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
