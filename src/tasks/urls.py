from django.urls import path
from tasks.views import (
    TaskListAPIView,
    TaskDetailAPIView,
    TaskReportAPIView,
    TaskStatsAPIView,
)

urlpatterns = [
    path("", TaskListAPIView.as_view(), name="task-list"),
    path("stats/", TaskStatsAPIView.as_view(), name="task-stats"),
    path("<int:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
    path("<int:pk>/report/", TaskReportAPIView.as_view(), name="task-report"),
]