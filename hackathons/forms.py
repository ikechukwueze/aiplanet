from django import forms
from .models import Hackathon, HackathonSubmission



class HackathonCreationForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        exclude = ["id"]


class HackathonChangeForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        exclude = ["id"]


class HackathonSubmissionCreationForm(forms.ModelForm):
    class Meta:
        model = HackathonSubmission
        exclude = ["id"]


class HackathonSubmissionChangeForm(forms.ModelForm):
    class Meta:
        model = HackathonSubmission
        exclude = ["id"]