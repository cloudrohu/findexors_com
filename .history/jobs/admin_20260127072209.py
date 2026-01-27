from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Job, JobApplicant, InterviewSchedule


# =====================================================
# INTERVIEW INLINE (ONE TO ONE)
# =====================================================
class InterviewInline(admin.StackedInline):
    model = InterviewSchedule
    extra = 0
    max_num = 1
    can_delete = False
    show_change_link = True

    exclude = ("job",)  # 🔒 job hidden (auto set)

    fieldsets = (
        ("📞 Interview Details", {
            "fields": (
                "interview_type",
                ("interview_date", "interview_time"),
                "duration_minutes",
                "assigned_to",
            )
        }),
        ("📍 Meeting Info", {
            "fields": (
                "meeting_link",
                "location",
            )
        }),
        ("📝 Status & Notes", {
            "fields": (
                "status",
                "remarks",
                ("whatsapp_sent", "reminder_sent"),
            )
        }),
    )

    readonly_fields = ("created_at", "updated_at")


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


# =====================================================
# JOB ADMIN
# =====================================================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id", "job_title", "company",
        "job_type", "work_location_type",
        "city", "status", "created_at",
    )

    list_filter = (
        "status", "job_type",
        "work_location_type", "city", "company",
    )

    search_fields = (
        "title__name",
        "company__company_name",
    )

    filter_horizontal = (
        "skills", "benefits",
        "assets", "documents", "languages",
    )

    readonly_fields = ("slug", "created_at", "updated_at")

    inlines = [JobApplicantInline]

    def job_title(self, obj):
        return obj.title.name if obj.title else "-"
    job_title.short_description = "Job Title"


# =====================================================
# JOB APPLICANT ADMIN (IMPORT / EXPORT READY)
# =====================================================
@admin.register(JobApplicant)
class JobApplicantAdmin(ImportExportModelAdmin):

    list_display = (
        "full_name", "job", "phone",
        "apply_source", "status", "applied_at",
    )

    list_filter = (
        "status", "apply_source",
        "job", "city",
    )

    search_fields = (
        "full_name", "phone",
        "email", "job__title__name",
    )

    readonly_fields = ("applied_at", "status_updated_at")

    inlines = [InterviewInline]


# =====================================================
# INTERVIEW ADMIN (STANDALONE)
# =====================================================
@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "applicant", "job",
        "interview_type",
        "interview_date",
        "interview_time",
        "status",
    )

    list_filter = (
        "status", "interview_type",
        "interview_date",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
    )

    readonly_fields = ("created_at", "updated_at")
