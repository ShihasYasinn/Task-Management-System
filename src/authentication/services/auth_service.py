from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class AuthService:

    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise Exception("Username and password are required")

        user = authenticate(username=username, password=password)

        if not user:
            from users.models import User
            if User.objects.filter(username=username).exists():
                raise Exception("Invalid credentials")
            else:
                user = User.objects.create_user(username=username, password=password, role="USER")
        
        if not user.is_active:
            raise Exception("Account is disabled")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
            }
        }

    @staticmethod
    def refresh_token(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        except TokenError:
            raise Exception("Invalid refresh token")

    @staticmethod
    def logout(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return True
        except TokenError:
            raise Exception("Invalid refresh token")