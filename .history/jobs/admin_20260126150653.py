from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_per_page = 25
    ordering = ("-created_at",)

    list_display = (
        "id",
        "job_title",
        "company",
        "job_type",
        "work_location_type",
        "openings",
        "salary_range",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "job_type",
        "work_location_type",
        "city",
        "category",
        "industry",
    )

    search_fields = (
        "company__company_name",
        "title__name",
        "city__name",
        "locality__name",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🏢 Company & Job", {
            "fields": ("company", "title", "category", "industry", "openings")
        }),
        ("📍 Location", {
            "fields": ("city", "locality", "work_location_type")
        }),
        ("🕒 Job Type & Timing", {
            "fields": (
                "job_type",
                "start_time",
                "end_time",
                "working_days",
            )
        }),
        ("💰 Salary", {
            "fields": ("salary_type", "salary_min", "salary_max")
        }),
        ("🧑 Candidate Preferences", {
            "fields": (
                "gender",
                "only_fresher",
                "min_experience_months",
                "max_experience_months",
            )
        }),
        ("🏷 Skills / Benefits", {
            "fields": (
                "skills",
                "benefits",
                "assets",
                "documents",
                "languages",
            )
        }),
        ("📝 Description", {
            "fields": ("description", "requirements")
        }),
        ("⚙ Status & Meta", {
            "fields": ("status", "created_by", "created_at", "updated_at")
        }),
    )

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    # ---------- Custom Columns ----------
    def job_title(self, obj):
        return obj.title.name if obj.title else "-"
    job_title.short_description = "Job Title"

    def salary_range(self, obj):
        return f"₹{obj.salary_min} - ₹{obj.salary_max}"
    salary_range.short_description = "Salary"
