from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import Account



class APITest(APITestCase):

    def setUp(self) -> None:
        self.account_details = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@mail.com",
            "role": Account.Role.PARTICIPANT,
            "password": "fakepassword",
            "confirm_password": "fakepassword",
        }

        self.existing_details = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@mail.com",
            "role": Account.Role.PARTICIPANT,
            "password": "fakepassword"
        }
        self.existing_account = Account.objects.create_user(**self.existing_details)
        self.account_signup_url = reverse("account_signup")
        self.account_login_url = reverse("account_login")


    def test_successful_account_signup(self):
        response = self.client.post(
            self.account_signup_url, self.account_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["first_name"], self.account_details["first_name"]
        )
        self.assertEqual(response.data["last_name"], self.account_details["last_name"])
        self.assertEqual(response.data["email"], self.account_details["email"])
        self.assertEqual(response.data["role"], self.account_details["role"])
    

    def test_failed_account_signup_with_incorrect_passwords(self):
        self.account_details["confirm_password"] = "password"
        response = self.client.post(
            self.account_signup_url, self.account_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_successful_account_login(self):
        login_details = {"email": self.existing_details["email"], "password": self.existing_details["password"]}
        response = self.client.post(
            self.account_login_url, login_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], login_details["email"])
        self.assertEqual(response.data["token"], Token.objects.get(user__email=login_details["email"]).key)


    def test_failed_login_with_incorrect_details(self):
        login_details = {"email": "janedoe@mail.com", "password": "wrongfakepassword"}
        response = self.client.post(
            self.account_login_url, login_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
