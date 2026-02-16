from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Job, JobApplicant, InterviewSchedule
from django.utils.html import format_html


class InterviewInline(admin.StackedInline):
    model = InterviewSchedule
    extra = 0
    max_num = 1
    can_delete = True

    readonly_fields = ("created_at", "updated_at", "job")

    fields = (
        "scheduled_datetime",
        "duration_minutes",
        "assigned_to",
        "status",
        "remarks",
        "whatsapp_sent",
        "reminder_sent",
        "confirmation_received",
    )


# =====================================================
# JOB APPLICANT INLINE (INSIDE JOB)
# =====================================================
class JobApplicantInline(admin.TabularInline):
    model = JobApplicant
    extra = 0
    show_change_link = True

    fields = (
        "full_name",
        "phone",
        "status",
        "apply_source",
        "applied_at",
    )

    readonly_fields = ("applied_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "company",
        "category",
        "industry",
        "job_type",
        "work_location_type",
        "city",
        "locality",
        "salary_min",
        "salary_max",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "job_type",
        "work_location_type",
        "city",
        "company",
        "industry",
        "category",
    )

    search_fields = (
        "title__name",
        "company__company_name",
        "city__name",
        "locality__name",
    )

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    readonly_fields = ("slug", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "company",
                "title",
                "category",
                "industry",
                "slug",
                "openings",
                "status",
            )
        }),

        ("Job Type & Location", {
            "fields": (
                "job_type",
                "work_location_type",
                "city",
                "locality",
                "working_days",
                "start_time",
                "end_time",
            )
        }),

        ("Experience & Salary", {
            "fields": (
                "gender",
                "min_experience_months",
                "max_experience_months",
                "salary_type",
                "salary_min",
                "salary_max",
            )
        }),

        ("Skills & Requirements", {
            "fields": (
                "skills",
                "benefits",
                "assets",
                "documents",
                "languages",
                "description",
                "requirements",
            )
        }),

        ("Meta", {
            "fields": (
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            )
        }),
    )

    inlines = [JobApplicantInline]
@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "job",
        "phone",
        "city",
        "status",
        "apply_source",
        "experience_months",
        "applied_at",
    )

    list_filter = (
        "status",
        "apply_source",
        "job",
        "city",
        "notice_period",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "job__title__name",
    )

    readonly_fields = (
        "applied_at",
        "status_updated_at",
    )

    fieldsets = (
        ("Candidate Info", {
            "fields": (
                "job",
                "user",
                "full_name",
                "phone",
                "email",
                "resume",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
            )
        }),

        ("Career Info", {
            "fields": (
                "experience_months",
                "current_company",
                "current_salary",
                "expected_salary",
                "notice_period",
                "expected_joining_date",
            )
        }),

        ("Application Details", {
            "fields": (
                "apply_source",
                "allow_whatsapp",
                "status",
                "cover_letter",
                "internal_notes",
            )
        }),

        ("Tracking", {
            "fields": (
                "applied_at",
                "status_updated_at",
            )
        }),
    )

    inlines = [InterviewInline]


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "applicant",
        "job",
        "scheduled_datetime",
        "interview_type",
        "assigned_to",
        "status",
        "confirmation_received",
    )

    list_filter = (
        "status",
        "interview_type",
        "assigned_to",
        "job",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
        "job__title__name",
    )

    readonly_fields = (
        "job",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "scheduled_datetime"
    ordering = ("-scheduled_datetime",)

    fieldsets = (
        ("Candidate & Assignment", {
            "fields": (
                "applicant",
                "job",
                "assigned_to",
            )
        }),

        ("Schedule Details", {
            "fields": (
                "scheduled_datetime",
                "interview_type",
                "duration_minutes",
                "rescheduled_from",
            )
        }),

        ("Meeting Info", {
            "fields": (
                "meeting_link",
                "location",
            )
        }),

        ("Status & CRM Tracking", {
            "fields": (
                "status",
                "remarks",
                "internal_feedback",
                "whatsapp_sent",
                "reminder_sent",
                "confirmation_received",
                "last_contacted_at",
                "next_followup_at",
            )
        }),

        ("Meta", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )
