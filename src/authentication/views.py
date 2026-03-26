from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.serializers import LoginSerializer, RefreshTokenSerializer, LogoutSerializer
from authentication.services.auth_service import AuthService
from commons.utils.response import APIResponse


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                APIResponse.error("Invalid data", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = AuthService.login(serializer.validated_data)
            return Response(
                APIResponse.success(data=data, message="Login successful"),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_401_UNAUTHORIZED
            )


class RefreshTokenAPIView(APIView):

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                APIResponse.error("Invalid data", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = AuthService.refresh_token(serializer.validated_data['refresh'])
            return Response(
                APIResponse.success(data=data, message="Token refreshed successfully"),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                APIResponse.error("Invalid data", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            AuthService.logout(serializer.validated_data['refresh'])
            return Response(
                APIResponse.success(message="Logged out successfully"),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
        }
        
        return Response(
            APIResponse.success(data=data),
            status=status.HTTP_200_OK
        )