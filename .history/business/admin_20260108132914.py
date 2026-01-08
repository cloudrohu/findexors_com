from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

# =====================================================
# AUTO USER MIXIN
# =====================================================

class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not change and not obj.created_by:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if hasattr(obj, "created_by") and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user
            if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
                obj.uploaded_by = request.user
            obj.save()
        formset.save_m2m()


# =====================================================
# FORMSET VALIDATIONS
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
# INLINES
# =====================================================

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1


class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# COMPANY ADMIN (MAIN)
# =====================================================

@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id", "company_name", "category",
        "city", "locality", 'address',"project",
        "contact_no", "status",
        "is_verified", "is_featured",
        "assigned_to", "created_at"
    )

    search_fields = ("company_name", "contact_no")
    list_filter = ("status", "category", "city", "locality", "project")

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "logo_preview",
        "slug",
    )

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "company_name", "contact_no", "whatsapp", "email",
                "category", "city", "locality", "sub_locality",
                "project", "address", "description",
                "logo", "logo_preview"
            )
        }),
        ("📊 Status", {
            "fields": (
                "status", "assigned_to",
                "is_active", "is_verified", "is_featured",
                "website", "google_map"
            )
        }),
        ("🕒 Audit", {
            "fields": ("slug", "created_at", "updated_at")
        }),
    )

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

    list_per_page = 20


# =====================================================
# OTHER ADMINS
# =====================================================

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
    )


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by")
    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
        "updated_at",
    )


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/company/followup_card_list.html"

    list_display = (
        "id", "company", "status",
        "followup_date", "assigned_to", "created_by"
    )

    search_fields = ("company__company_name",)
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/company/meeting_card_list.html"

    list_display = (
        "id", "company", "status",
        "meeting_date", "assigned_to", "created_by"
    )

    search_fields = ("company__company_name",)
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")




@admin.register(Approx)
class ApproxAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")
    readonly_fields = (
        "create_at",
        "update_at",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")
    readonly_fields = (
        "create_at",
        "update_at",
    )


@admin.register(Error)
class ErrorAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Images)
class ImagesAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(Faq)
class FaqAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    readonly_fields = (
        "create_at",
        "update_at",
    )
