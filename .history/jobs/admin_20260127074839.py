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


# =====================================================
# INTERVIEW ADMIN (STANDALONE)
# =====================================================
# jobs/admin.py

from django.contrib import admin
from .models import InterviewSchedule


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    # =========================
    # LIST PAGE (TABLE VIEW)
    # =========================
    list_display = (
        "id",
        "applicant_name",
        "job",
        "interview_type",
        "interview_datetime",
        "assigned_to",
        "status_badge",
        "whatsapp_sent",
        "reminder_sent",
    )

    list_filter = (
        "status",
        "interview_type",
        "interview_date",
        "assigned_to",
        "job",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
        "applicant__email",
        "job__title__name",
    )

    list_select_related = ("applicant", "job", "assigned_to")

    date_hierarchy = "interview_date"

    ordering = ("-interview_date", "-interview_time")

    readonly_fields = ("created_at", "updated_at")

    # =========================
    # FORM LAYOUT (DETAIL PAGE)
    # =========================
    fieldsets = (
        ("👤 Candidate & Job", {
            "fields": (
                "applicant",
                "job",
                "assigned_to",
            )
        }),
        ("📞 Interview Details", {
            "fields": (
                "interview_type",
                ("interview_date", "interview_time"),
                "duration_minutes",
            )
        }),
        ("📍 Meeting Information", {
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
        ("⚙ Meta", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    # =========================
    # CUSTOM COLUMNS
    # =========================
    def applicant_name(self, obj):
        return obj.applicant.full_name
    applicant_name.short_description = "Candidate"
    applicant_name.admin_order_field = "applicant__full_name"

    def interview_datetime(self, obj):
        return f"{obj.interview_date} {obj.interview_time}"
    interview_datetime.short_description = "Interview Time"

    def status_badge(self, obj):
        color_map = {
            "scheduled": "#2563eb",
            "rescheduled": "#d97706",
            "completed": "#16a34a",
            "cancelled": "#dc2626",
            "no_show": "#6b7280",
        }
        color = color_map.get(obj.status, "#334155")
        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;'
            'background:{};color:white;font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_badge.short_description = "Status"

    # =========================
    # UX IMPROVEMENTS
    # =========================
    list_per_page = 25
    save_on_top = True
