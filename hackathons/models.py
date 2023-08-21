import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from accounts.models import Account


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hackathon(BaseModel):
    class SubmissionType(models.TextChoices):
        IMAGE = "IMAGE", "IMAGE"
        FILE = "FILE", "FILE"
        LINK = "LINK", "LINK"

    organiser = models.ForeignKey(Account, related_name="hackathons", on_delete=models.CASCADE)
    participants = models.ManyToManyField(Account, blank=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    background_image = models.ImageField(upload_to="background_images/")
    hackathon_image = models.ImageField(upload_to="hackathon_images/")
    submission_type = models.CharField(max_length=7, choices=SubmissionType.choices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prize = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date')),
                name='start_date_before_end_date'
            ),
            models.CheckConstraint(
                check=Q(prize__gte=Decimal("100.00")),
                name='positive_prize'
            )
        ]



class HackathonSubmission(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="hackathon_submissions")
    participant = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="participant_submissions")
    submission_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    submission_object_id = models.UUIDField()
    submission = GenericForeignKey('submission_object_type', 'submission_object_id')
    
    class Meta:
        indexes = [
            models.Index(fields=["submission_object_type", "submission_object_id"]),
        ]





class BaseSubmissionModel(BaseModel):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    participant = models.ForeignKey(Account, on_delete=models.CASCADE)
    submission_name = models.CharField(max_length=100)
    summary = models.TextField()

    class Meta:
        abstract = True



class FileSubmission(BaseSubmissionModel):
    submission = models.FileField(upload_to='submissions/files/')



class ImageSubmission(BaseSubmissionModel):
    submission = models.ImageField(upload_to='submissions/images/')



class LinkSubmission(BaseSubmissionModel):
    submission = models.URLField()