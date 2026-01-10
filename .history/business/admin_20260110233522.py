from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db import models

from import_export.admin import ImportExportModelAdmin
from .resources import CompanyResource

from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)


# =====================================================
# ✅ FILTER: Contact Number
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
            return queryset.filter(models.Q(contact_no__isnull=True) | models.Q(contact_no=""))
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
# ✅ INLINE FORMSET VALIDATIONS
# =====================================================
class FollowupInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("status") in ["New Followup", "Re Followup"]:
                active += 1
        if active > 1:
            raise ValidationError("❌ Sirf 1 Active Followup allowed hai")


class MeetingInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("status") in ["New Meeting", "Re Meeting"]:
                active += 1
        if active > 1:
            raise ValidationError("❌ Sirf 1 Active Meeting allowed hai")


# =====================================================
# ✅ INLINES
# =====================================================
class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


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
# ✅ COMPANY ADMIN (CARD VIEW)
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, ImportExportModelAdmin):
    change_list_template = "admin/business/company/change_list.html"
    resource_class = CompanyResource

    list_display = (
        "id", "company_name", "category", "city", "locality",
        "project", "contact_no", "status",
        "is_verified", "is_featured", "assigned_to", "created_at",
    )

    search_fields = ("company_name", "contact_no")

    list_filter = (
        "status", "category", "city", "locality",
        "project", "assigned_to",
        ContactNumberFilter,
    )

    readonly_fields = (
        "created_by", "updated_by",
        "created_at", "updated_at",
        "logo_preview", "slug",
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
        ("📊 Status & Assignment", {
            "fields": (
                "status", "assigned_to",
                "is_active", "is_verified", "is_featured",
                "website", "google_map",
            )
        }),
        ("🕒 Audit Info", {
            "fields": ("slug", "created_at", "updated_at")
        }),
    )

    inlines = [
        ImagesInline, SocialLinkInline, FaqInline,
        CommentInline, VoiceRecordingInline, VisitInline,
        FollowupInline, MeetingInline,
    ]

    list_per_page = 20


# =====================================================
# ✅ OTHER ADMINS
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
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    readonly_fields = ("uploaded_by", "uploaded_at", "updated_at")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "update_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "update_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Approx)
class ApproxAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")


@admin.register(SocialLink)
class SocialLinkAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")


@admin.register(Error)
class ErrorAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Images)
class ImagesAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(Faq)
class FaqAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "questions")
