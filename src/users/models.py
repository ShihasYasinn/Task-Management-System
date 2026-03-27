from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("SUPERADMIN", "SuperAdmin"),
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="USER")
    assigned_admin = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )

    def is_superadmin(self):
        return self.role == "SUPERADMIN" or self.is_superuser

    def is_admin(self):
        return self.role == "ADMIN"

    def is_user(self):
        return self.role == "USER"