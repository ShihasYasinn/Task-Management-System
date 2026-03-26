from django.urls import path
from admin_panel.views import (
    dashboard, users_list, tasks_list, task_create, user_create
)

urlpatterns = [
    path("", dashboard, name="admin-dashboard"),
    path("users/", users_list, name="admin-users"),
    path("users/create/", user_create, name="admin-user-create"),
    path("tasks/", tasks_list, name="admin-tasks"),
    path("tasks/create/", task_create, name="admin-task-create"),
]