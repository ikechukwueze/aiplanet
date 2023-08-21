from django.test import TestCase
from rest_framework import serializers
from accounts.models import Account
from accounts.serializers import AccountSignUpSerializer, LoginSerializer



class TestAccountSignUpSerializerValidation(TestCase):
    def test_valid_signup_data(self):
        valid_signup_details = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@mail.com",
            "role": Account.Role.PARTICIPANT,
            "password": "fakepassword",
            "confirm_password": "fakepassword",
        }
        serializer = AccountSignUpSerializer(data=valid_signup_details)
        self.assertTrue(serializer.is_valid(raise_exception=True))
    

    def test_invalid_signup_data(self):
        invalid_signup_details = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@mail.com",
            "role": Account.Role.PARTICIPANT,
            "password": "fakepassword",
            "confirm_password": "fakepassword121212",
        }
        serializer = AccountSignUpSerializer(data=invalid_signup_details)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class TestLoginSerializerValidation(TestCase):
    def setUp(self) -> None:
        existing_details = {
            "first_name": "Jenny",
            "last_name": "Doe",
            "email": "jennydoe@mail.com",
            "role": Account.Role.PARTICIPANT,
            "password": "fakepassword"
        }
        Account.objects.create_user(**existing_details)
        

    def test_valid_login_data(self):
        valid_login_details = {
            "email": "jennydoe@mail.com",
            "password": "fakepassword"
        }
        serializer = LoginSerializer(data=valid_login_details)
        self.assertTrue(serializer.is_valid(raise_exception=True))
    

    def test_invalid_login_data(self):
        invalid_login_details = {
            "email": "jennydoe@mail.com",
            "password": "fakepassword1223"
        }
        serializer = LoginSerializer(data=invalid_login_details)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)