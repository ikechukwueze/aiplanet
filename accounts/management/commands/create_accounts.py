from django.core.management.base import BaseCommand
from accounts.models import Account



class Command(BaseCommand):

    def handle(self, *args, **options):
        organiser_account = {
            "first_name": "The",
            "last_name": "Organiser",
            "email": "organiser@email.com",
            "role": Account.Role.ORGANISER,
            "password": "easypassword",
        }

        participant_1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "role": Account.Role.PARTICIPANT,
            "password": "easypassword",
        }

        participant_2 = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@email.com",
            "role": Account.Role.PARTICIPANT,
            "password": "easypassword",
        }

        Account.objects.create_superuser(**organiser_account)
        Account.objects.create_user(**participant_1)
        Account.objects.create_user(**participant_2)

        print(f"Email: {organiser_account['email']}")
        print(f"password: {organiser_account['password']}")
