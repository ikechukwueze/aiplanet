from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from accounts.models import Account


# Create your tests here.


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.organiser_account = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe1@email.com",
            "role": Account.Role.ORGANISER,
            "password": "easypassword",
        }

        self.participant_account = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe2@email.com",
            "role": Account.Role.PARTICIPANT,
            "password": "easypassword",
        }


    def test_create_superuser_account(self):
        account_details = self.organiser_account
        superuser_account = Account.objects.create_superuser(**account_details)
        password = account_details.pop("password")
        
        self.assertEqual(Account.objects.count(), 1)
        self.assertTrue(superuser_account.is_admin)
        self.assertTrue(check_password(password, superuser_account.password))
        for field, value in account_details.items():
            self.assertEqual(getattr(superuser_account, field), value)
        
        
    def test_create_user_account(self):
        account_details = self.participant_account
        account = Account.objects.create_user(**account_details)
        password = account_details.pop("password")
        
        self.assertEqual(Account.objects.count(), 1)
        self.assertFalse(account.is_admin)
        self.assertTrue(check_password(password, account.password))
        for field, value in account_details.items():
            self.assertEqual(getattr(account, field), value)
    

    def test_create_user_raises_value_error_for_null_params(self):
        params = {"email": "", "first_name":"", "last_name": "", "role": ""}
        for key, value in params.items():
            self.participant_account[key] = value
            with self.assertRaises(ValueError):
                Account.objects.create_user(**self.participant_account)
    

    def test_cannot_create_admin_account_with_participant_role(self):
        participant = Account.objects.create_user(**self.participant_account)
        participant.is_admin = True
        with self.assertRaises(ValidationError):
            participant.save()


    def test_token_created_with_new_account(self):
        organiser = Account.objects.create_superuser(**self.organiser_account)
        participant = Account.objects.create_user(**self.participant_account)
        self.assertTrue(Token.objects.filter(user=organiser).exists())
        self.assertTrue(Token.objects.filter(user=participant).exists())
        self.assertEqual(Token.objects.get(user=organiser).key, organiser.get_token())
        self.assertEqual(Token.objects.get(user=participant).key, participant.get_token())