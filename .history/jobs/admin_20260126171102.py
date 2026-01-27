from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Job


from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "job_title_display", "company", "job_type", "status", "created_at")
    list_filter = ("status", "job_type", "work_location_type", "city")
    search_fields = ("company__company_name", "title__name")
    filter_horizontal = ("skills", "benefits", "assets", "documents", "languages")
    readonly_fields = ("created_at", "updated_at")

    def job_title_display(self, obj):
        return obj.title.name if obj.title else "-"
    job_title_display.short_description = "Job Title"

    fieldsets = (
        ("🏢 Company & Job", {"fields": ("company", "title", "category", "industry", "openings")}),
        ("📍 Location", {"fields": ("city", "locality", "work_location_type")}),
        ("🕒 Timing", {"fields": ("job_type", "start_time", "end_time", "working_days")}),
        ("💰 Salary", {"fields": ("salary_type", "salary_min", "salary_max")}),
        ("🏷 Tags", {"fields": ("skills", "benefits", "assets", "documents", "languages")}),
        ("📝 Content", {"fields": ("description", "requirements")}),
        ("⚙ Status", {"fields": ("status", "created_by", "created_at", "updated_at")}),
    )