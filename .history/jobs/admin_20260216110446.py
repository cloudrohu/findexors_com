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
        "gender",
        "salary_type",
        "salary_min",
        "salary_max",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "company",
        "category",
        "industry",
        "job_type",
        "work_location_type",
        "gender",
        "salary_type",
        "city",
        "locality",
        "working_days",
        "created_at",
    )

    search_fields = (
        "title__name",
        "company__company_name",
        "city__name",
        "locality__name",
    )

    autocomplete_fields = (
        "company",
        "title",
        "industry",
        "city",
        "locality",
    )

    list_select_related = (
        "company",
        "title",
        "industry",
        "city",
        "locality",
    )

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    readonly_fields = ("slug", "created_at", "updated_at")

    date_hierarchy = "created_at"

    inlines = [JobApplicantInline]



@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "job",
        "phone",
        "city",
        "locality",
        "experience_months",
        "notice_period",
        "apply_source",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "apply_source",
        "job",
        "city",
        "locality",
        "notice_period",
        "allow_whatsapp",
        "applied_at",
        "status_updated_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "job__title__name",
        "current_company",
    )

    autocomplete_fields = (
        "job",
        "city",
        "locality",
        "user",
    )

    list_select_related = (
        "job",
        "city",
        "locality",
        "user",
    )

    readonly_fields = (
        "applied_at",
        "status_updated_at",
    )

    date_hierarchy = "applied_at"

    inlines = [InterviewInline]


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "applicant",
        "job",
        "interview_type",
        "scheduled_datetime",
        "assigned_to",
        "status",
        "whatsapp_sent",
        "confirmation_received",
    )

    list_filter = (
        "status",
        "interview_type",
        "assigned_to",
        "job",
        "whatsapp_sent",
        "reminder_sent",
        "confirmation_received",
        "scheduled_datetime",
        "created_at",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
        "job__title__name",
        "assigned_to__name",
    )

    autocomplete_fields = (
        "applicant",
        "assigned_to",
    )

    list_select_related = (
        "applicant",
        "job",
        "assigned_to",
    )

    readonly_fields = (
        "job",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "scheduled_datetime"
    ordering = ("-scheduled_datetime",)
