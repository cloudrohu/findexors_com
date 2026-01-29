from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Job, JobApplicant, InterviewSchedule
from django.utils.html import format_html


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
class JobApplicantAdmin(admin.ModelAdmin):

#class JobApplicantAdmin(ImportExportModelAdmin):
    change_list_template = "admin/jobs/jobapplicant/change_list.html"

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

@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    change_list_template = "admin/jobs/interviewschedule/change_list_cards.html"
    preserve_filters = True
    list_per_page = 50

    list_display = (
        "id",
        "applicant",
        "job",
        "scheduled_datetime",
        "assigned_to",
        "status",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
        "job__title__name",
    )

    list_filter = (
        "status",
        "assigned_to",
        "job",
    )

    readonly_fields = ("job", "created_at", "updated_at")
    date_hierarchy = "scheduled_datetime"
    ordering = ("-scheduled_datetime",)

    fieldsets = (
        ("Candidate & Job", {
            "fields": ("applicant", "job", "assigned_to")
        }),
        ("Schedule", {
            "fields": ("scheduled_datetime", "duration_minutes")
        }),
        ("Meeting", {
            "fields": ("meeting_link", "location")
        }),
        ("Status", {
            "fields": (
                "status",
                "remarks",
                "internal_feedback",
                "whatsapp_sent",
                "reminder_sent",
                "confirmation_received",
            )
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    # 🔥 REALTYPMS STYLE MAGIC SEARCH
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            term = search_term.upper().strip()

            # 👉 Interview ID (INT012)
            if term.startswith("INT"):
                num = term.replace("INT", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            # 👉 Applicant ID (APP045)
            if term.startswith("APP"):
                num = term.replace("APP", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(applicant__id=int(num))

            # 👉 Job ID (JOB099)
            if term.startswith("JOB"):
                num = term.replace("JOB", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(job__id=int(num))

            # 👉 Phone quick search
            if term.isdigit():
                queryset |= self.model.objects.filter(
                    applicant__phone__icontains=term
                )

        return queryset, use_distinct
