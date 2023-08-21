import os
from rest_framework import serializers
from accounts.serializers import AccountSerializer
from accounts.models import Account
from .models import (
    Hackathon,
    HackathonSubmission,
    ImageSubmission,
    FileSubmission,
    LinkSubmission,
)
from .utils import validate_hackathon, check_submission_exists



class SimpleHackathonSerializer(serializers.ModelSerializer):
    organiser = serializers.CharField()

    class Meta:
        model = Hackathon
        fields = [
            "id",
            "organiser",
            "title",
            "description",
            "start_date",
            "end_date",
            "prize",
        ]



class HackathonSerializer(serializers.ModelSerializer):
    organiser = AccountSerializer(read_only=True)
    participants = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Hackathon
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]



class GenericSubmissionSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, FileSubmission):
            serializer = FileSubmissionSerializer(value)

        elif isinstance(value, ImageSubmission):
            serializer = ImageSubmissionSerializer(value)

        elif isinstance(value, LinkSubmission):
            serializer = LinkSubmissionSerializer(value)

        else:
            raise Exception("Unexpected type of submission object")

        return serializer.data



class HackathonSubmissionSerializer(serializers.ModelSerializer):
    hackathon = serializers.CharField(read_only=True)
    participant = serializers.CharField(read_only=True)
    submission = GenericSubmissionSerializer(read_only=True)

    class Meta:
        model = HackathonSubmission
        exclude = ["submission_object_id", "submission_object_type"]



class FileSubmissionSerializer(serializers.ModelSerializer):
    hackathon = serializers.CharField(read_only=True)
    participant = serializers.CharField(read_only=True)

    class Meta:
        model = FileSubmission
        fields = "__all__"

    def validate_submission(self, value):
        img_extensions = [".png", ".jpg", ".jpeg"] # can be extended
        _, file_extension = os.path.splitext(value.name)

        if file_extension in img_extensions:
            raise serializers.ValidationError(
                f"Invalid file extension. '{file_extension}' is not an allowed extension."
            )

        return value

    def validate(self, attrs):
        hackathon_id = self.context["hackathon_id"]
        participant_id = self.context["participant_id"]
        hackathon = validate_hackathon(hackathon_id)
        check_submission_exists(hackathon_id, participant_id)
        participant = Account.objects.get(id=participant_id)
        attrs["hackathon"] = hackathon
        attrs["participant"] = participant
        return attrs

    
    def create(self, validated_data):
        submission_obj = self.Meta.model.objects.create(**validated_data)

        HackathonSubmission.objects.create(
            hackathon=validated_data["hackathon"],
            participant=validated_data["participant"],
            submission=submission_obj
        )
        return submission_obj



class ImageSubmissionSerializer(FileSubmissionSerializer):
    class Meta:
        model = ImageSubmission
        fields = "__all__"

    def validate_submission(self, value):
        return value
    


class LinkSubmissionSerializer(FileSubmissionSerializer):
    class Meta:
        model = LinkSubmission
        fields = "__all__"
    
    def validate_submission(self, value):
        return value



class HackathonEnrollmentSerializer(serializers.Serializer):
    hackathon_id = serializers.IntegerField()
    participant_id = serializers.UUIDField()

    def validate(self, attrs):
        hackathon_id = attrs["hackathon_id"]
        _ = validate_hackathon(hackathon_id)
        return attrs
