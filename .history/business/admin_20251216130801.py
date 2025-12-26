from django.contrib import admin
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)
from response.models import Staff

class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.created_by:
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


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id", "company_name", "category",
        "city", "locality", "sub_locality",
        "contact_no", "status",
        "is_verified", "is_featured",
        "assigned_to", "created_at"
    )

    list_filter = (
        "status", "category",
        "city", "locality", "sub_locality",
        "is_verified", "is_featured",
        "assigned_to"
    )

    search_fields = (
        "company_name", "contact_no",
        "city__title", "locality__title",
        "sub_locality__title"
    )

    readonly_fields = (
        "slug", "created_at", "updated_at", "logo_preview"
    )

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "company_name", "category",
                "city", "locality", "sub_locality",
                "address", "description",
                "logo", "logo_preview"
            )
        }),
        ("📞 Contact Details", {
            "fields": (
                "contact_no", "whatsapp",
                "email", "website", "google_map"
            )
        }),
        ("📊 Status & Assignment", {
            "fields": (
                "status",
                "assigned_to",
                "is_active", "is_verified", "is_featured"
            )
        }),
        ("🧠 SEO", {
            "fields": ("slug",)
        }),
        ("🕒 Audit Info", {
            "fields": (
                "created_by", "updated_by",
                "created_at", "updated_at"
            )
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



@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to")
    list_filter = ("status", "assigned_to")


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to")
    list_filter = ("status", "assigned_to")


@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "socia_site", "link")


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "image")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")
