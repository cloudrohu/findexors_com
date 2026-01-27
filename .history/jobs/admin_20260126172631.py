# jobs/admin.py
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "job_type", "status", "created_at")
    list_filter = ("status", "job_type", "work_location_type", "city")
    search_fields = ("company__company_name", "title__name")
    filter_horizontal = ("skills", "benefits", "assets", "documents", "languages")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🏢 Job Info", {"fields": ("company", "title", "category", "industry", "openings")}),
        ("📍 Location", {"fields": ("city", "locality", "work_location_type")}),
        ("🕒 Timing", {"fields": ("job_type", "start_time", "end_time", "working_days")}),
        ("💰 Salary", {"fields": ("salary_type", "salary_min", "salary_max")}),
        ("👤 Candidate", {"fields": ("gender", "min_experience_months", "max_experience_months")}),
        ("🏷 Tags", {"fields": ("skills", "benefits", "assets", "documents", "languages")}),
        ("📝 Content", {"fields": ("description", "requirements")}),
        ("⚙ Meta", {"fields": ("status", "created_by", "created_at", "updated_at")}),
    )
