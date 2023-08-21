import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.images import ImageFile
from accounts.models import Account
from hackathons.models import (
    Hackathon,
    HackathonSubmission,
    FileSubmission,
    ImageSubmission,
    LinkSubmission,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cwd = os.path.abspath(os.path.dirname(__file__))

        organiser = Account.objects.get(email="organiser@email.com")
        participant_1 = Account.objects.get(email="johndoe@email.com")
        participant_2 = Account.objects.get(email="janedoe@email.com")

        b_image = open(os.path.join(cwd, "image.jpg"), "rb")
        h_image = open(os.path.join(cwd, "image copy.jpg"), "rb")

        submission_types = [
            Hackathon.SubmissionType.FILE,
            Hackathon.SubmissionType.IMAGE,
            Hackathon.SubmissionType.LINK,
        ]

        for index, submission_type in enumerate(submission_types):
            hackathon_details = {
                "organiser": organiser,
                "title": f"hackathon {index+1}",
                "description": "a hard hackathon",
                "submission_type": submission_type,
                "background_image": ImageFile(b_image, name="image.jpg"),
                "hackathon_image": ImageFile(h_image, name="image.jpg"),
                "start_date": "2023-08-25",
                "end_date": "2023-10-10",
                "prize": "10000.00",
            }
            Hackathon.objects.create(**hackathon_details)
        
        b_image.close()
        h_image.close()

        participants = [participant_1, participant_2]

        h1 = Hackathon.objects.get(id=1)
        h2 = Hackathon.objects.get(id=2)
        h3 = Hackathon.objects.get(id=3)

        h1.participants.add(*participants)
        h2.participants.add(*participants)
        h3.participants.add(participant_1)

        image = open(os.path.join(cwd, "image.jpg"), "rb")
        file = open(os.path.join(cwd, "data.txt"), "rb")
        link = "http://fakelink.com"

        file_submission = FileSubmission.objects.create(
            hackathon=h1,
            participant=participant_1,
            submission=File(file, "data.txt"),
            submission_name="My solution",
            summary="My summary",
        )
        image_submission = ImageSubmission.objects.create(
            hackathon=h2,
            participant=participant_2,
            submission=ImageFile(image, name="image.jpg"),
            submission_name="My solution",
            summary="My summary",
        )
        link_submission = LinkSubmission.objects.create(
            hackathon=h3,
            participant=participant_1,
            submission=link,
            submission_name="My solution",
            summary="My summary",
        )

        d = {
            file_submission: [h1, participant_1],
            image_submission: [h2, participant_2],
            link_submission: [h3, participant_1],
        }

        for key, value in d.items():
            h, p = value
            HackathonSubmission.objects.create(
                hackathon=h, participant=p, submission=key
            )
        
        image.close()
        file.close()

        print("done.")
