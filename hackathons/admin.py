from django.contrib import admin
from .forms import (
    HackathonCreationForm,
    HackathonChangeForm,
    HackathonSubmissionCreationForm,
    HackathonSubmissionChangeForm,
)
from .models import (
    Hackathon,
    HackathonSubmission,
    FileSubmission,
    ImageSubmission,
    LinkSubmission,
)

# Register your models here.


class HackathonAdmin(admin.ModelAdmin):
    form = HackathonChangeForm
    add_form = HackathonCreationForm
    list_display = ["title", "id", "submission_type", "start_date", "end_date", "prize"]


class HackathonSubmissionAdmin(admin.ModelAdmin):
    form = HackathonSubmissionChangeForm
    add_form = HackathonSubmissionCreationForm
    list_display = ["hackathon", "participant"]


class FileSubmissionAdmin(admin.ModelAdmin):
    list_display = ["hackathon", "participant", "submission_name"]


class ImageSubmissionAdmin(FileSubmissionAdmin):
    pass


class LinkSubmissionAdmin(FileSubmissionAdmin):
    pass



admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(HackathonSubmission, HackathonSubmissionAdmin)
admin.site.register(FileSubmission, FileSubmissionAdmin)
admin.site.register(ImageSubmission, ImageSubmissionAdmin)
admin.site.register(LinkSubmission, LinkSubmissionAdmin)
