from typing import Union
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Account




class AccountSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Account
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs: dict) -> Union[serializers.ValidationError, dict]:
        password = attrs["password"]
        confirm_password = attrs.pop("confirm_password")

        if not password == confirm_password:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return attrs

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> Union[serializers.ValidationError, dict]:
        account = authenticate(**attrs)
        if not account:
            raise serializers.ValidationError(
                {
                    "email": "Incorrect email or password",
                    "password": "Incorrect email or password.",
                }
            )
        if not account.is_active:
            raise serializers.ValidationError(
                {"email": "This account has been suspended."}
            )
        attrs["account"] = account
        return attrs


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "role"]