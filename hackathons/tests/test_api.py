import os
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from accounts.models import Account
from hackathons.models import Hackathon, HackathonSubmission
from hackathons.serializers import HackathonSerializer, SimpleHackathonSerializer, HackathonSubmissionSerializer, FileSubmissionSerializer
from hackathons.views import SubmitHackathonSolution


class ApiTests(APITestCase):
    fixtures = ["accounts.json", "authtoken.json", "hackathons.json"]

    def setUp(self) -> None:
        self.cwd = os.path.abspath(os.path.dirname(__file__))

        self.organiser = Account.objects.get(email="admin@admin.com")
        self.jane_participant_acc = Account.objects.get(email="janedoe@live.com")
        self.john_participant_acc = Account.objects.get(email="johndoe@live.com")
        self.new_hackathon = Hackathon.objects.get(id=4)

        self.organiser_client = APIClient()
        self.jane_client = APIClient()
        self.john_client = APIClient()

        self.organiser_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.organiser.get_token()
        )
        self.jane_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.jane_participant_acc.get_token()
        )
        self.john_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.john_participant_acc.get_token()
        )


    def test_list_hackathons(self):
        response = self.client.get(reverse("list-hackathons"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Hackathon.objects.count())


    def test_create_hackathon(self):
        background_image = open(f"{self.cwd}/test_data/image.jpg", "rb")
        hackathon_image = open(f"{self.cwd}/test_data/image.jpg", "rb")

        hackathon_details = {
            "title": "hackathon",
            "description": "a hard hackathon",
            "background_image": background_image,
            "hackathon_image": hackathon_image,
            "submission_type": "LINK",
            "start_date": "2023-08-25",
            "end_date": "2023-10-10",
            "prize": "10000.00",
        }

        response = self.organiser_client.post(
            reverse("create-hackathon"), data=hackathon_details
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        background_image.close()
        hackathon_image.close()


    def test_participant_cannot_create_hackathon(self):
        background_image = open(f"{self.cwd}/test_data/image.jpg", "rb")
        hackathon_image = open(f"{self.cwd}/test_data/image.jpg", "rb")

        hackathon_details = {
            "title": "hackathon",
            "description": "a hard hackathon",
            "background_image": background_image,
            "hackathon_image": hackathon_image,
            "submission_type": "LINK",
            "start_date": "2023-08-25",
            "end_date": "2023-10-10",
            "prize": "10000.00",
        }

        response = self.jane_client.post(
            reverse("create-hackathon"), data=hackathon_details
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Only organisers can create hackathons"}
        )

    
    def test_participant_can_register_for_hackathon(self):
        response = self.jane_client.post(reverse("enrol-for-hackathon", kwargs={"hackathon_id": self.new_hackathon.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, SimpleHackathonSerializer(self.new_hackathon).data)
        self.assertEqual(self.new_hackathon.participants.first(), self.jane_participant_acc)
    

    def test_organiser_cannot_register_for_hackathon(self):
        response = self.organiser_client.post(reverse("enrol-for-hackathon", kwargs={"hackathon_id": self.new_hackathon.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Only participants allowed"}
        )


    def test_participant_can_submit_solution_to_registered_hackathon(self):
        self.new_hackathon.participants.add(self.jane_participant_acc)

        file = open(f"{self.cwd}/test_data/data.txt", "rb")
        data = {
            "submission_name": "Solution",
            "summary": "My solution",
            "submission": file
        }
        url = reverse("submit-hackathon-solution", kwargs={"hackathon_id": self.new_hackathon.id})
        response = self.jane_client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            HackathonSubmission.objects.filter(hackathon=self.new_hackathon, participant=self.jane_participant_acc).exists()
        )
        file.close()
    

    def test_correct_serializer_is_used_for_submission(self):
        self.new_hackathon.participants.add(self.jane_participant_acc)

        file = open(f"{self.cwd}/test_data/data.txt", "rb")
        expected_serializer = FileSubmissionSerializer
        
        data = {
            "submission_name": "Solution",
            "summary": "My solution",
            "submission": file
        }
        url = reverse("submit-hackathon-solution", kwargs={"hackathon_id": self.new_hackathon.id})

        request = APIRequestFactory().post(url, data=data)
        force_authenticate(request, user=self.jane_participant_acc, token=self.jane_participant_acc.get_token())
        
        view = SubmitHackathonSolution()
        view.setup(request)
        view.hackathon_id = self.new_hackathon.id
        serializer_used = view.get_serializer_class()

        self.assertEqual(serializer_used, expected_serializer)
        file.close()
    

    def test_participant_cannot_submit_wrong_type_to_registered_hackathon(self):
        self.new_hackathon.participants.add(self.jane_participant_acc)

        file = open(f"{self.cwd}/test_data/image.jpg", "rb")
        link = "http://fakelink.com"

        submissions = [file, link]

        for wrong_submission in submissions:
            data = {
                "submission_name": "Solution",
                "summary": "My solution",
                "submission": wrong_submission
            }
            url = reverse("submit-hackathon-solution", kwargs={"hackathon_id": self.new_hackathon.id})
            response = self.jane_client.post(path=url, data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        file.close()


    def test_participant_cannot_submit_solution_to_unregistered_hackathon(self):
        file = open(f"{self.cwd}/test_data/data.txt", "rb")
        data = {
            "submission_name": "Solution",
            "summary": "My solution",
            "submission": file
        }
        url = reverse("submit-hackathon-solution", kwargs={"hackathon_id": self.new_hackathon.id})
        response = self.john_client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        file.close()


    def test_participant_can_list_submissions(self):
        jane_submissions = HackathonSubmission.objects.filter(participant=self.jane_participant_acc)
        response = self.jane_client.get(reverse("all-participant-submissions"))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, HackathonSubmissionSerializer(jane_submissions, many=True).data)
    

    def test_participant_can_retrieve_single_submission(self):
        jane_submissions = HackathonSubmission.objects.filter(participant=self.jane_participant_acc, hackathon__id=1).first()
        response = self.jane_client.get(reverse("single-participant-submission", kwargs={"hackathon_id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, HackathonSubmissionSerializer(jane_submissions).data)


    def test_organiser_can_list_submissions_for_all_hackathons(self):
        all_submissions = HackathonSubmission.objects.filter(hackathon__organiser=self.organiser)
        response = self.organiser_client.get(reverse("all-hackathon-submissions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), all_submissions.count())
    

    def test_organiser_can_list_submissions_for_single_hackathons(self):
        submissions = HackathonSubmission.objects.filter(hackathon__organiser=self.organiser, hackathon__id=1)
        response = self.organiser_client.get(reverse("hackathon-submissions", kwargs={"hackathon_id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), submissions.count())


    def test_list_enrolled_hackathons(self):
        janes_hackathons = Hackathon.objects.filter(participants=self.jane_participant_acc)
        response = self.jane_client.get(reverse("enrolled-hackathons"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), janes_hackathons.count())
