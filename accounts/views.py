from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSignUpSerializer, LoginSerializer

# Create your views here.



class AccountSignUpView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = AccountSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        account_details = {
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "role": account.role
        }
        return Response(account_details, status=status.HTTP_201_CREATED)


class AccountLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data["account"]
        account_details = {
            "email": account.email,
            "token": account.get_token(),
        }
        return Response(account_details, status=status.HTTP_200_OK)
