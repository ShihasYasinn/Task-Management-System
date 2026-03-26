from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    identifier = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username") or data.get("identifier")

        if not username:
            raise serializers.ValidationError({
                "identifier": "Username or identifier is required"
            })

        data["username"] = username
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()