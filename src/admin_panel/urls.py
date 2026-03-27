from django.urls import path
from admin_panel.views import (
    dashboard, users_list, tasks_list, task_create, user_create, admin_login, admin_logout, support, profile
)

urlpatterns = [
    path("login/", admin_login, name="admin-login"),
    path("logout/", admin_logout, name="admin-logout"),
    path("", dashboard, name="admin-dashboard"),
    path("users/", users_list, name="admin-users"),
    path("users/create/", user_create, name="admin-user-create"),
    path("tasks/", tasks_list, name="admin-tasks"),
    path("tasks/create/", task_create, name="admin-task-create"),
    path("support/", support, name="admin-support"),
    path("profile/", profile, name="admin-profile"),
]