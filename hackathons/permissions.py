from rest_framework import permissions
from accounts.models import Account
from hackathons.models import Hackathon



class IsOrganiser(permissions.BasePermission):
    message = "Only organisers can create hackathons"

    def has_permission(self, request, view):
        return request.user.role == Account.Role.ORGANISER


class IsHackathonOrganiserOrRetrieveOnly(permissions.BasePermission):
    message = "Only hackathon organiser can change hackathon details"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.organiser == request.user


class IsParticipant(permissions.BasePermission):
    message = "Only participants allowed"

    def has_permission(self, request, view):
        return request.user.role == Account.Role.PARTICIPANT


class IsHackathonParticipant(permissions.BasePermission):
    message = "You are not enrolled in this hackathon"

    def has_permission(self, request, view):
        hackathon_id = view.kwargs.get("hackathon_id")
        is_hackathon_participant = (
            Hackathon.objects.filter(id=hackathon_id)
            .filter(participants=request.user)
            .exists()
        )
        return is_hackathon_participant
