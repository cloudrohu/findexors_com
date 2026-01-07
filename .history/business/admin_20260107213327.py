from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils import translation

from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

# Django 4/5 compatibility
if not hasattr(translation, "ugettext_lazy"):
    translation.ugettext_lazy = translation.gettext_lazy


# =====================================================
# AUTO USER MIXIN
# =====================================================
class AutoUserAdminMixin(admin.ModelAdmin):
    """
    Auto set created_by / updated_by / uploaded_by
    """

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.created_by:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


# =====================================================
# INLINE VALIDATIONS
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
            raise ValidationError("❌ Ek company ke liye sirf 1 Followup allowed hai.")


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
            raise ValidationError("❌ Ek company ke liye sirf 1 Meeting allowed hai.")


# =====================================================
# INLINE MODELS
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
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# COMPANY ADMIN
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin):
    list_display = (
        "id",
        "company_name",
        "category",
        "city",
        "locality",
        "sub_locality",
        "project",
        "contact_no",
        "status",
        "is_verified",
        "is_featured",
        "assigned_to",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        "sub_locality",
        "project",
        "assigned_to",
        "is_verified",
        "is_featured",
    )

    search_fields = ("company_name", "contact_no")

    readonly_fields = ("slug", "created_at", "updated_at", "logo_preview")

    inlines = [
        ImagesInline,
        SocialLinkInline,
        FaqInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline,
    ]


# =====================================================
# FOLLOWUP ADMIN (Company fields shown)
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin):
    list_display = (
        "id",
        "company_name",
        "company_city",
        "company_locality",
        "company_contact",
        "company_category",
        "status",
        "followup_date",
        "assigned_to",
        "created_by",
        "update_at",
    )

    list_filter = ("status", "assigned_to", "company__city", "company__category")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def company_name(self, obj):
        return obj.company.company_name

    def company_city(self, obj):
        return obj.company.city

    def company_locality(self, obj):
        return obj.company.locality

    def company_contact(self, obj):
        return obj.company.contact_no

    def company_category(self, obj):
        return obj.company.category


# =====================================================
# MEETING ADMIN (Company fields shown)
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin):
    list_display = (
        "id",
        "company_name",
        "company_city",
        "company_locality",
        "company_contact",
        "company_category",
        "status",
        "meeting_date",
        "assigned_to",
        "created_by",
        "update_at",
    )

    list_filter = ("status", "assigned_to", "company__city", "company__category")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def company_name(self, obj):
        return obj.company.company_name

    def company_city(self, obj):
        return obj.company.city

    def company_locality(self, obj):
        return obj.company.locality

    def company_contact(self, obj):
        return obj.company.contact_no

    def company_category(self, obj):
        return obj.company.category


# =====================================================
# SIMPLE ADMINS (NO AUDIT FIELDS)
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")
