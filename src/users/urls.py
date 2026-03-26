from django.urls import path
from users.views import (
    UserListAPIView,
    UserDetailAPIView,
    ChangePasswordAPIView,
    UserStatsAPIView,
)

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("stats/", UserStatsAPIView.as_view(), name="user-stats"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
]