from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin

from .models import GoogleCompany, Comment, VoiceRecording, Visit, Followup, Meeting
from .resources import GoogleCompanyResource


class PhoneFilter(admin.SimpleListFilter):
    title = "Phone"
    parameter_name = "phone_status"

    def lookups(self, request, model_admin):
        return (("yes", "Has Phone"), ("no", "No Phone"))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(phone__isnull=True).exclude(phone="")
        if self.value() == "no":
            return queryset.filter(models.Q(phone__isnull=True) | models.Q(phone=""))
        return queryset


@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportModelAdmin):
    resource_class = GoogleCompanyResource

    list_display = (
        "id", "name", "phone", "category_text",
        "city_text", "state", "postal_code",
        "rating", "reviews", "business_status",
        "created_at",
    )
    search_fields = ("name", "phone", "place_id", "google_id", "cid")
    list_filter = ("business_status", "country", "state", PhoneFilter)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 25
