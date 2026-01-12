from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin

from .models import GoogleCompany, Comment, VoiceRecording, Visit, Followup, Meeting
from .resources import GoogleCompanyResource


# =====================================================
# ✅ FILTER: Phone Status
# =====================================================
class PhoneFilter(admin.SimpleListFilter):
    title = "Phone"
    parameter_name = "phone_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Phone"),
            ("no", "No Phone"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(phone__isnull=True).exclude(phone="")
        if self.value() == "no":
            return queryset.filter(models.Q(phone__isnull=True) | models.Q(phone=""))
        return queryset


# =====================================================
# ✅ AUTO USER MIXIN
# =====================================================
class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not change and not getattr(obj, "created_by", None):
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# ✅ INLINES
# =====================================================
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    readonly_fields = ("uploaded_at", "uploaded_by")


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1
    readonly_fields = ("uploaded_at", "updated_at", "uploaded_by")


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 1
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# ✅ GOOGLE COMPANY ADMIN
# =====================================================
@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportModelAdmin):
    resource_class = GoogleCompanyResource

    list_display = (
        "id",
        "name",
        "phone",
        "city_text",
        "state",
        "postal_code",
        "status",
        "category_text",
        "rating",
        "reviews",
        "business_status",
        "created_at",
    )

    search_fields = ("name", "phone", "place_id", "google_id", "cid", "address")
    list_filter = ("business_status", "country", "status", "state", PhoneFilter)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "status",
                "name", "name_for_emails",
                "category", "category_text",
                "city", "city_text",
                "locality",
                "type",
                "phone", "website",
                "address", "street",
                "postal_code", "state", "country",
                "logo",
            )
        }),
        ("⭐ Google Stats", {
            "fields": (
                "rating", "reviews",
                "business_status", "working_hours",
            )
        }),
        ("🔎 IDs", {
            "fields": ("place_id", "google_id", "cid")
        }),
        ("📍 Geo", {
            "fields": ("latitude", "longitude")
        }),
        ("🕒 Audit", {
            "fields": ("created_at", "updated_at")
        }),
    )

    inlines = [CommentInline, VoiceInline, VisitInline, FollowupInline, MeetingInline]


# =====================================================
# ✅ COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "create_at")
    search_fields = ("company__name", "company__phone", "comment")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


# =====================================================
# ✅ VOICE ADMIN
# =====================================================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")
    readonly_fields = ("uploaded_at", "uploaded_by")


# =====================================================
# ✅ VISIT ADMIN
# =====================================================
@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")


# =====================================================
# ✅ FOLLOWUP ADMIN
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "update_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


# =====================================================
# ✅ MEETING ADMIN
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "update_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")
