from django.contrib import admin
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

# =====================================================
# AUTO USER MIXIN (NO MANUAL SELECT EVER)
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
# INLINE MODELS (TABs)
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
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0
    exclude = ("uploaded_by", "uploaded_at")


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    exclude = ("uploaded_by", "uploaded_at", "updated_at")


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# COMPANY ADMIN (MAIN)
# =====================================================
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
                "contact_no",
                "website", "google_map"
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
