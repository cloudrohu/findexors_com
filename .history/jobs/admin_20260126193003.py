# jobs/admin.py

from django.contrib import admin
from .models import InterviewSchedule
from .models import Job, JobApplicant,InterviewSchedule


# =========================
# INTERVIEW INLINE (ONE TO ONE)
# =========================
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
    )


# =========================
# JOB ADMIN
# =========================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    # 🔹 LIST PAGE
    list_display = (
        "id",
        "job_title",
        "company",
        "job_type",
        "work_location_type",
        "city",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "job_type",
        "work_location_type",
        "city",
        "company",
    )

    search_fields = (
        "title__name",
        "company__company_name",
    )

    # ❌ REMOVE prepopulated_fields
    # prepopulated_fields = {"slug": ("company",)}

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    # 🔒 READ ONLY
    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    # 🧱 FORM STRUCTURE
    fieldsets = (

        ("🏢 Job Details", {
            "fields": (
                "company",
                "title",
                "category",
                "industry",
                "openings",
                "slug",
            )
        }),

        ("📍 Location & Type", {
            "fields": (
                "job_type",
                "work_location_type",
                "city",
                "locality",
            )
        }),

        ("💰 Salary", {
            "fields": (
                "salary_type",
                ("salary_min", "salary_max"),
            )
        }),

        ("🕒 Working Time", {
            "fields": (
                ("start_time", "end_time"),
                "working_days",
            )
        }),

        ("🏷 Skills & Requirements", {
            "fields": (
                "skills",
                "benefits",
                "assets",
                "documents",
                "languages",
            )
        }),

        ("📝 Content", {
            "fields": (
                "description",
                "requirements",
            )
        }),

        ("⚙ Meta", {
            "fields": (
                "status",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            )
        }),
    )

    # 🧠 CUSTOM COLUMN
    def job_title(self, obj):
        return obj.title.name if obj.title else "-"
    job_title.short_description = "Job Title"

# =========================
# JOB APPLICANT ADMIN
# =========================
@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "job",
        "phone",
        "apply_source",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "apply_source",
        "job",
        "city",
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

    inlines = [InterviewInline]

    fieldsets = (
        ("👤 Candidate Info", {
            "fields": (
                "job",
                "user",
                "full_name",
                "phone",
                "email",
                ("city", "locality"),
            )
        }),
        ("💼 Experience", {
            "fields": (
                "experience_months",
                "current_company",
                ("current_salary", "expected_salary"),
                "notice_period",
                "expected_joining_date",
            )
        }),
        ("📄 Resume & Notes", {
            "fields": (
                "resume",
                "cover_letter",
                "internal_notes",
            )
        }),
        ("📌 Application Status", {
            "fields": (
                "apply_source",
                "allow_whatsapp",
                "status",
                "applied_at",
                "status_updated_at",
            )
        }),
    )




# interviews/admin.py



@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "applicant",
        "job",
        "interview_type",
        "interview_date",
        "interview_time",
        "status",
    )

    list_filter = (
        "status",
        "interview_type",
        "interview_date",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
    )

    readonly_fields = ("created_at", "updated_at")
