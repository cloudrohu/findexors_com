from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db import models

from import_export.admin import ImportExportModelAdmin

from .models import (
    GoogleCompany,
    Company,
    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,
)


# =====================================================
# ✅ CUSTOM FILTER: Contact Number
# =====================================================
class ContactNumberFilter(admin.SimpleListFilter):
    title = "Contact Number"
    parameter_name = "contact_no_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Number"),
            ("no", "No Number"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(contact_no__isnull=True).exclude(contact_no="")
        if self.value() == "no":
            return queryset.filter(
                models.Q(contact_no__isnull=True) | models.Q(contact_no="")
            )
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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if hasattr(obj, "created_by") and not getattr(obj, "created_by", None):
                obj.created_by = request.user
            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user
            if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
                obj.uploaded_by = request.user
            obj.save()
        formset.save_m2m()


# =====================================================
# ✅ INLINE FORMSETS
# =====================================================
class FollowupInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        return


class MeetingInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        return


# =====================================================
# ✅ INLINES
# =====================================================
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by")


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")


class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 0
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 0
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# ✅ GOOGLE COMPANY ADMIN
# =====================================================
@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportModelAdmin):
    list_display = (
        "id", "name", "phone", "category_text",
        "city_text", "state", "postal_code",
        "rating", "reviews", "business_status", "created_at",
    )
    search_fields = ("name", "phone", "place_id", "google_id", "cid")
    list_filter = ("business_status", "country", "state")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25


# =====================================================
# ✅ COMPANY ADMIN
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, ImportExportModelAdmin):

    list_display = (
        "id", "company_name", "category",
        "city", "locality", "project",
        "contact_no", "status",
        "rating", "reviews_count",
        "is_verified", "is_featured",
        "assigned_to", "created_at",
    )

    list_filter = (
        "status", "category",
        "city", "locality", "project",
        "assigned_to",
        ContactNumberFilter,
    )

    search_fields = ("company_name", "contact_no")

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()
            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

        return queryset, use_distinct

    readonly_fields = (
        "created_by", "updated_by",
        "created_at", "updated_at",
        "slug", "logo_preview",
    )

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "company_name", "contact_no", "email",
                "category", "city", "locality", "sub_locality",
                "project", "address", "description",
                "logo", "logo_preview",
            )
        }),
        ("⭐ Google / Rating", {
            "fields": (
                "rating", "reviews_count",
                "business_status_raw",
                "google_map", "googlemap_status",
                "website",
            )
        }),
        ("📊 Status & Assignment", {
            "fields": (
                "status", "assigned_to",
                "is_active", "is_verified", "is_featured",
            )
        }),
        ("🕒 Audit", {
            "fields": (
                "slug",
                "created_by", "updated_by",
                "created_at", "updated_at",
            )
        }),
    )

    inlines = [
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline,
    ]

    list_per_page = 20


# =====================================================
# ✅ COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "company__contact_no", "comment")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("uploaded_by", "uploaded_at")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("visit_type", "visit_status", "company__city", "company__locality")
    readonly_fields = ("uploaded_by", "uploaded_at", "updated_at")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "created_by", "update_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("status", "assigned_to", "company__category", "company__city", "company__locality", "company__project")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "created_by", "update_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("status", "assigned_to", "company__category", "company__city", "company__locality", "company__project")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")
