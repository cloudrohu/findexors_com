from django.contrib import admin
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

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
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user
            obj.save()
        formset.save_m2m()


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
            raise ValidationError(
                "❌ Ek company ke liye sirf 1 Active Followup allowed hai."
            )



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
            raise ValidationError(
                "❌ Ek company ke liye sirf 1 Active Meeting allowed hai."
            )


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


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    exclude = ("uploaded_by", "uploaded_at")


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1
    exclude = ("uploaded_by", "uploaded_at", "updated_at")


class FollowupInline(admin.TabularInline):
    model = Followup
    formset = FollowupInlineFormSet   # ⭐ IMPORTANT
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.TabularInline):
    model = Meeting
    formset = MeetingInlineFormSet    # ⭐ IMPORTANT
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# COMPANY ADMIN
# =====================================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'js/admin_dependent_dropdown.js',
        )

    list_display = (
        "id", "company_name", "category",
        "city", "locality", "sub_locality", "project",
        "contact_no", "status",
        "is_verified", "is_featured",
        "assigned_to", "created_at"
    )

    list_filter = (
        "status", "category",
        "city", "locality", "sub_locality", "project",
        "is_verified", "is_featured",
        "assigned_to"
    )

    search_fields = ("company_name", "contact_no")

    readonly_fields = ("slug", "created_at", "updated_at", "logo_preview")

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                 "status","assigned_to","company_name", "contact_no", "whatsapp", "email", "category",
                "city", "locality", "sub_locality", "project",
                "address", "description",
                "logo", "logo_preview"
            )
        }),
        
        ("📊 Status & Assignment", {
            "fields": (
                
                "is_active", "is_verified", "is_featured","website", "google_map"
            )
        }),
        ("🕒 Audit Info", {"fields": ("slug","created_at", "updated_at")}),
    )

    inlines = [
        ImagesInline,
        SocialLinkInline,
        FaqInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline
    ]

    list_per_page = 20

# =====================================================
# OTHER ADMINS
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_by", "uploaded_at")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status")
    readonly_fields = ("uploaded_by", "uploaded_at")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to")
    list_filter = ("status", "assigned_to")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")