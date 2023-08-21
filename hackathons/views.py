from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from .serializers import (
    HackathonSerializer,
    HackathonSubmissionSerializer,
    HackathonEnrollmentSerializer,
    SimpleHackathonSerializer,
    FileSubmissionSerializer,
    ImageSubmissionSerializer,
    LinkSubmissionSerializer,
)
from .models import Hackathon, HackathonSubmission
from .permissions import (
    IsOrganiser,
    IsHackathonOrganiserOrRetrieveOnly,
    IsParticipant,
    IsHackathonParticipant,
)

# Create your views here.



class ListHackathons(ListAPIView):
    serializer_class = HackathonSerializer

    def get_queryset(self):
        queryset = (
            Hackathon.objects.prefetch_related("organiser", "participants")
            .all()
            .order_by("-created_at")
        )
        return queryset



class CreateHackathon(CreateAPIView):
    serializer_class = HackathonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrganiser]

    def get_queryset(self):
        queryset = Hackathon.objects.prefetch_related("organiser", "participants").all()
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organiser=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RetrieveUpdateDeleteHackathon(RetrieveUpdateDestroyAPIView):
    serializer_class = HackathonSerializer
    queryset = Hackathon.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsHackathonOrganiserOrRetrieveOnly]



class HackathonEnrollment(APIView):
    serializer_class = HackathonEnrollmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant]

    def post(self, request, **kwargs):
        data = {
            "participant_id": request.user.id,
            "hackathon_id": kwargs["hackathon_id"],
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        participant_id = serializer.validated_data["participant_id"]
        hackathon_id = serializer.validated_data["hackathon_id"]
        participant = Account.objects.get(id=participant_id)
        hackathon = Hackathon.objects.get(id=hackathon_id)
        hackathon.participants.add(participant)
        return Response(
            SimpleHackathonSerializer(hackathon).data, status=status.HTTP_201_CREATED
        )



class ListEnrolledHackathons(ListAPIView):
    serializer_class = SimpleHackathonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        queryset = Hackathon.objects.filter(
            participants=self.request.user
        ).select_related("organiser")
        return queryset



class ListSubmissionsForAllHackathons(ListAPIView):
    serializer_class = HackathonSubmissionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOrganiser]

    def get_queryset(self):
        account = self.request.user
        submissions = HackathonSubmission.objects.select_related(
            "hackathon__organiser", "participant"
        )
        return submissions.filter(hackathon__organiser=account)



class ListSubmissionsForSingleHackathon(ListAPIView):
    serializer_class = HackathonSubmissionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOrganiser]

    def get_queryset(self):
        account = self.request.user
        hackathon_id = self.kwargs["hackathon_id"]
        submissions = HackathonSubmission.objects.select_related(
            "hackathon__organiser", "participant"
        )
        return submissions.filter(
            hackathon__organiser=account, hackathon__id=hackathon_id
        )



class ListParticipantSubmissionsForAllHackathons(ListAPIView):
    serializer_class = HackathonSubmissionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        account = self.request.user
        submissions = HackathonSubmission.objects.select_related(
            "hackathon__organiser", "participant"
        )
        return submissions.filter(participant=account)



class RetrieveParticipantSubmissionForHackathon(RetrieveAPIView):
    serializer_class = HackathonSubmissionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant]
    lookup_field = "hackathon_id"

    def get_queryset(self):
        account = self.request.user
        submissions = HackathonSubmission.objects.select_related(
            "hackathon__organiser", "participant"
        )
        return submissions.filter(participant=account)



class SubmitHackathonSolution(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsHackathonParticipant]
    hackathon_id = None

    def get_serializer_class(self):
        serializers = {
            Hackathon.SubmissionType.LINK: LinkSubmissionSerializer,
            Hackathon.SubmissionType.IMAGE: ImageSubmissionSerializer,
            Hackathon.SubmissionType.FILE: FileSubmissionSerializer,
        }
        try:
            hackathon = Hackathon.objects.get(id=self.hackathon_id)
        except Hackathon.DoesNotExist:
            return None
        else:
            return serializers[hackathon.submission_type]

    @transaction.atomic
    def post(self, request, **kwargs):
        self.hackathon_id = kwargs["hackathon_id"]
        serializer_class = self.get_serializer_class()

        if serializer_class is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {
            "participant_id": request.user.id,
            "hackathon_id": self.hackathon_id,
        }
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
