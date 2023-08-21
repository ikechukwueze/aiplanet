from typing import Union
from uuid import uuid4
from hackathons.models import Hackathon, HackathonSubmission
from django.utils import timezone
from rest_framework import serializers


def validate_hackathon(hackathon_id: int) -> Union[Hackathon, serializers.ValidationError]:
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
    except Hackathon.DoesNotExist:
        raise serializers.ValidationError({"hackathon_id": "Hackathon does not exist"})
    else:
        if hackathon.end_date < timezone.now():
            raise serializers.ValidationError({"hackathon_id": "Hackathon has ended"})
    return hackathon


def check_submission_exists(hackathon_id: int, participant_id: uuid4)-> Union[None, serializers.ValidationError]:
    if HackathonSubmission.objects.filter(hackathon=hackathon_id, participant=participant_id).exists():
        raise serializers.ValidationError({"hackathon_id": "Already submitted"})