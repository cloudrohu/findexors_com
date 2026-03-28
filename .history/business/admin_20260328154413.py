from django.contrib import admin
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Followup, Meeting, Images, Faq
)


# =====================================================
# ✅ AUTO USER MIXIN (GLOBAL)
# =====================================================
class AutoUserAdminMixin:

    def save_model(self, request, obj, form, change):

        if hasattr(obj, "created_by") and not change:
            if not obj.created_by:
                obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:

            if hasattr(obj, "created_by") and not obj.pk:
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
                obj.uploaded_by = request.user

            obj.save()

        formset.save_m2m()


# =====================================================
# ✅ INLINE CLASSES
# =====================================================
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


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
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1
    max_num = 1
    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


class ImageInline(admin.StackedInline):
    model = Images
    extra = 1


class FaqInline(admin.StackedInline):
    model = Faq
    extra = 1
    readonly_fields = ("create_at", "update_at")


# =====================================================
# ✅ COMPANY ADMIN (CARD UI)
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    change_list_template = "admin/business/company_card_list.html"
    list_per_page = 200
    preserve_filters = True

    list_display = (
        "id", "status", "company_name", "contact_no",
        "category", "city", "locality", "assigned_to",
        "rating", "reviews_count", "updated_at",
    )

    search_fields = ("company_name", "contact_no", "email", "website", "address")

    list_filter = (
        "status", "category", "city", "locality",
        "assigned_to", "is_active", "is_verified", "is_featured",
    )

    readonly_fields = (
        "created_at", "updated_at",
        "created_by", "updated_by",
        "logo_preview",
    )

    ordering = ("-created_at",)

    inlines = [
        CommentInline,
        VoiceInline,
        VisitInline,
        FollowupInline,
        MeetingInline,
        ImageInline,
        FaqInline,
    ]


# =====================================================
# ✅ COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/comment_card_list.html"


    list_display = ("id", "company", "comment", "create_at", "created_by")
    search_fields = ("company__company_name", "comment")
    list_filter = ("company__city", "company__status")

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


# =====================================================
# ✅ VOICE ADMIN
# =====================================================
@admin.register(VoiceRecording)
class VoiceAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/voice_card_list.html"


    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name",)
    list_filter = ("company__city",)

    readonly_fields = ("uploaded_at", "uploaded_by")


# =====================================================
# ✅ VISIT ADMIN
# =====================================================
@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id", "company", "visit_type",
        "visit_status", "uploaded_by", "uploaded_at"
    )

    search_fields = ("company__company_name",)
    list_filter = ("visit_status", "visit_type", "company__city")

    readonly_fields = ("uploaded_at", "updated_at", "uploaded_by")


# =====================================================
# ✅ FOLLOWUP ADMIN
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/company_card_list.html"

    list_display = (
        "id", "company", "status",
        "followup_date", "assigned_to", "update_at"
    )

    search_fields = ("company__company_name",)
    list_filter = ("status", "assigned_to", "company__city")

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


# =====================================================
# ✅ MEETING ADMIN
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/business/meeting_card_list.html"


    list_display = (
        "id", "company", "status",
        "meeting_date", "assigned_to", "created_by"
    )

    search_fields = ("company__company_name",)
    list_filter = ("status", "assigned_to", "company__city")

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")


# =====================================================
# ✅ IMAGE ADMIN
# =====================================================
@admin.register(Images)
class ImageAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = ("id", "company", "title", "image")
    search_fields = ("company__company_name", "title")


# =====================================================
# ✅ FAQ ADMIN
# =====================================================
@admin.register(Faq)
class FaqAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = ("id", "company", "questions", "create_at")
    search_fields = ("company__company_name", "questions")

    readonly_fields = ("create_at", "update_at")