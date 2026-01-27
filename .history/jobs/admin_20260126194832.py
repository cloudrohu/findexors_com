from django.contrib import admin
from .models import Job, JobApplicant, InterviewSchedule



class InterviewInline(admin.StackedInline):
    model = InterviewSchedule
    extra = 0
    max_num = 1
    can_delete = False
    show_change_link = True

    fields = (
        "interview_type",
        ("interview_date", "interview_time"),
        "duration_minutes",
        "assigned_to",
        "meeting_link",
        "location",
        "status",
        "remarks",
        ("whatsapp_sent", "reminder_sent"),
    )

    readonly_fields = ("created_at", "updated_at")


class JobApplicantInline(admin.StackedInline):
    model = JobApplicant
    extra = 0
    show_change_link = True
    readonly_fields = ("applied_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id", "job_title", "company",
        "job_type", "work_location_type",
        "city", "status", "created_at",
    )

    list_filter = ("status", "job_type", "work_location_type", "city", "company")
    search_fields = ("title__name", "company__company_name")

    filter_horizontal = ("skills", "benefits", "assets", "documents", "languages")
    readonly_fields = ("slug", "created_at", "updated_at")

    inlines = [JobApplicantInline]

    def job_title(self, obj):
        return obj.title.name if obj.title else "-"


@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):

    list_display = ("full_name", "job", "phone", "apply_source", "status", "applied_at")
    list_filter = ("status", "apply_source", "job", "city")
    search_fields = ("full_name", "phone", "email")

    readonly_fields = ("applied_at", "status_updated_at")

    inlines = [InterviewInline]


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "applicant", "job",
        "interview_type",
        "interview_date", "interview_time",
        "status",
    )

    list_filter = ("status", "interview_type", "interview_date")
    search_fields = ("applicant__full_name", "applicant__phone")
