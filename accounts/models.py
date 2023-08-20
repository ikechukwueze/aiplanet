import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .manager import AccountManager



class Account(AbstractBaseUser):
    class Role(models.TextChoices):
        ORGANISER = "ORGANISER", "ORGANISER"
        PARTICIPANT = "PARTICIPANT", "PARTICIPANT"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    signup_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self) -> bool:
        return self.is_admin
    

    def get_token(self) -> str:
        token = Token.objects.get(user=self).key
        return token


    def clean(self) -> None:
        if self.role is None:
            raise ValidationError("Role can not have a null value")
        
        if self.is_admin and self.role == self.Role.PARTICIPANT:
            raise ValidationError("A participant can not have admin privileges.")


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
