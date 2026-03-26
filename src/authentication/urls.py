from django.urls import path
from authentication.views import (
    LoginAPIView,
    RefreshTokenAPIView,
    LogoutAPIView,
    ProfileAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]