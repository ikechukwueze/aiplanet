import os
from datetime import datetime, timedelta
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from accounts.models import Account
from hackathons.models import Hackathon, HackathonSubmission, FileSubmission, ImageSubmission, LinkSubmission


# Create your tests here.


class ModelTest(TestCase):
    fixtures = ["accounts.json"]
    
    def setUp(self) -> None:
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.organiser = Account.objects.get(email="admin@admin.com")
        self.participant = Account.objects.get(email="janedoe@live.com")
        self.submission_types = [
            Hackathon.SubmissionType.FILE,
            Hackathon.SubmissionType.IMAGE,
            Hackathon.SubmissionType.LINK
        ]

        self.hackathon_details = {
            "organiser": self.organiser,
            "title": "hackathon",
            "description": "a hard hackathon",
            "submission_type": "LINK",
            "background_image": f"{self.cwd}/test_data/image.jpg",
            "hackathon_image": f"{self.cwd}/test_data/image.jpg",
            "start_date": "2023-08-25",
            "end_date": "2023-10-10",
            "prize": "10000.00",
        }


    def test_create_hackathon(self):
        for index, submission_type in enumerate(self.submission_types):
            d = {"title": f"hackathon_{index}", "submission_type": submission_type}
            self.hackathon_details.update(d)
            Hackathon.objects.create(**self.hackathon_details)
        
        self.assertEqual(Hackathon.objects.count(), 3)
    

    def test_new_hackathon_prize_contrainst(self):
        data = self.hackathon_details
        data["prize"] = "10.0"

        with self.assertRaises(IntegrityError):
            Hackathon.objects.create(**data)
    
    def test_hackathon_start_date_before_end_date_constraint(self):
        start_date = datetime.strptime(self.hackathon_details["start_date"], '%Y-%m-%d')
        wrong_start_date = start_date - timedelta(days=3)
        
        data = self.hackathon_details
        data["end_date"] = str(wrong_start_date)

        with self.assertRaises(IntegrityError):
            Hackathon.objects.create(**data) 
    

    def test_create_hackathon_submissions(self):
        image = f"{self.cwd}/test_data/image.jpg"
        file = f"{self.cwd}/test_data/data.txt"
        link = "http://fakelink.com"

        hackathons = []

        for index, submission_type in enumerate(self.submission_types):
            d = {"title": f"hackathon_{index}", "submission_type": submission_type}
            self.hackathon_details.update(d)
            hackathon = Hackathon.objects.create(**self.hackathon_details)
            hackathon.participants.add(self.participant)
            hackathons.append(hackathon)
        
        file_submission = FileSubmission.objects.create(hackathon=hackathons[0], participant=self.participant, submission=file)
        image_submission = ImageSubmission.objects.create(hackathon=hackathons[1], participant=self.participant, submission=image)
        link_submission = LinkSubmission.objects.create(hackathon=hackathons[2], participant=self.participant, submission=link)

        d = {hackathons[0]: file_submission, hackathons[1]: image_submission, hackathons[2]: link_submission}
        
        for key, value in d.items():
            HackathonSubmission.objects.create(hackathon=key, participant=self.participant, submission=value)
        
        self.assertEqual(HackathonSubmission.objects.count(), 3)