from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AccountChangeForm, AccountCreationForm
from .models import Account

# Register your models here.


class AccountAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
        "is_admin",
        "is_active",
        "signup_date",
    ]
    list_filter = ["is_admin", "role"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "is_admin",
                    "is_active",
                    "password",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "is_admin",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
