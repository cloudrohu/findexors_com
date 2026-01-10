from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin

from .models import GoogleCompany, Comment, VoiceRecording, Visit, Followup, Meeting
from .resources import GoogleCompanyResource




# =====================================================
# ✅ FILTER: Phone
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
# ✅ AUTO USER ADMIN MIXIN
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
    extra = 0
    exclude = ("created_by", "updated_by")


class VoiceInline(admin.StackedInline):
    model = VoiceRecording
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by")


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 0
    max_num = 1


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 0
    max_num = 1


# =====================================================
# ✅ GOOGLE COMPANY ADMIN (MAIN)
# =====================================================
@admin.register(GoogleCompany)
class GoogleCompanyAdmin(AutoUserAdminMixin, ImportExportModelAdmin):

    resource_class = GoogleCompanyResource

    list_display = (
        "id",
        "name",
        "phone",
        "category_text",
        "city_text",
        "state",
        "postal_code",
        "rating",
        "reviews",
        "status",
        "is_verified",
        "is_featured",
        "assigned_to",
        "created_at",
    )

    search_fields = ("name", "phone", "place_id", "google_id", "cid")
    list_filter = ("status", "business_status", "country", "state", PhoneFilter, "assigned_to", "is_verified", "is_featured")

    readonly_fields = ("slug", "created_at", "updated_at", "logo_preview")

    fieldsets = (
        ("🏢 Basic Info", {
            "fields": (
                "name", "name_for_emails",
                "category_text", "type",
                "phone", "website",
                "address", "street",
                "city_text", "state", "postal_code", "country",
                "logo", "logo_preview",
            )
        }),
        ("⭐ Google Stats", {
            "fields": (
                "rating", "reviews",
                "business_status", "working_hours",
                "place_id", "google_id", "cid",
            )
        }),
        ("📌 CRM Status", {
            "fields": (
                "status",
                "assigned_to",
                "is_active",
                "is_verified",
                "is_featured",
            )
        }),
        ("🕒 Audit", {
            "fields": ("slug", "created_by", "updated_by", "created_at", "updated_at")
        }),
    )

    inlines = [CommentInline, VoiceInline, VisitInline, FollowupInline, MeetingInline]
    ordering = ("-created_at",)
    list_per_page = 25


# =====================================================
# ✅ OTHER ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "create_at", "created_by")
    search_fields = ("company__name", "company__phone", "comment")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")
    readonly_fields = ("uploaded_at", "uploaded_by")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "update_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "update_at")
    search_fields = ("company__name", "company__phone")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")
