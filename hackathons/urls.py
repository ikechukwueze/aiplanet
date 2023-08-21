from django.urls import path
from . import views



urlpatterns = [
    path("", views.ListHackathons.as_view(), name="list-hackathons"),
    path("create/", views.CreateHackathon.as_view(), name="create-hackathon"),
    path("<int:pk>/", views.RetrieveUpdateDeleteHackathon.as_view(), name="retrieve-update-delete-hackathon"),
    path("<int:hackathon_id>/enrol/", views.HackathonEnrollment.as_view(), name="enrol-for-hackathon"),
    path("enrolled-hackathons/", views.ListEnrolledHackathons.as_view(), name="enrolled-hackathons"),
    #path("submissions/", views.ListHackathonSubmissions.as_view(), name="all-hackathon-submissions"),
    path("<int:hackathon_id>/submit/", views.SubmitHackathonSolution.as_view(), name="submit-hackathon-solution"),

    path("organiser/hackathon-submissions/", views.ListSubmissionsForAllHackathons.as_view(), name="all-hackathon-submissions"),
    path("organiser/hackathon-submissions/<int:hackathon_id>", views.ListSubmissionsForSingleHackathon.as_view(),  name="hackathon-submissions"),

    path("participant/hackathon-submissions/", views.ListParticipantSubmissionsForAllHackathons.as_view(), name="all-participant-submissions"),
    path("participant/hackathon-submissions/<int:hackathon_id>", views.RetrieveParticipantSubmissionForHackathon.as_view(), name="single-participant-submission"),
]