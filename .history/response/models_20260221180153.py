from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Staff,
    Response,
    Meeting,
    Followup,
    Comment,
    VoiceRecording,
)

# =====================================================
# 🔹 AUTO USER MIXIN
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
            if hasattr(obj, "created_by") and not obj.created_by:
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()
        formset.save_m2m()


# =====================================================
# 🔹 RESPONSE ADMIN
# =====================================================

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0
    show_change_link = True


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 0
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    show_change_link = True


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0
    show_change_link = True


@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
    ]

    list_display = (
        "mr_id",
        "status",
        "lead_source",
        "contact_no",
        "contact_persone",
        "business_name",
        "assigned_to",
        "is_converted",
        "create_at",
    )

    search_fields = (
        "contact_no",
        "contact_persone",
        "business_name",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "city",
        "locality",
        "is_converted",
        "create_at",
    )

    ordering = ("-create_at",)
    date_hierarchy = "create_at"

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
        "converted_at",
    )

    filter_horizontal = ("requirement_types",)

    def mr_id(self, obj):
        return format_html("<b style='color:#2563eb;'>MR{}</b>", str(obj.id).zfill(3))
    mr_id.short_description = "Response ID"


# =====================================================
# 🔹 MEETING ADMIN
# =====================================================

@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "status",
        "meeting_date",
        "assigned_to",
        "create_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "status",
        "assigned_to",
        "meeting_date",
    )

    ordering = ("-meeting_date",)

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
    )


# =====================================================
# 🔹 FOLLOWUP ADMIN
# =====================================================

@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "status",
        "followup_date",
        "assigned_to",
        "create_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "status",
        "assigned_to",
        "followup_date",
    )

    ordering = ("-followup_date",)

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
    )


# =====================================================
# 🔹 COMMENT ADMIN
# =====================================================

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "comment_short",
        "created_by",
        "create_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    ordering = ("-create_at",)

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
    )

    def comment_short(self, obj):
        return obj.comment[:50] if obj.comment else ""
    comment_short.short_description = "Comment"


# =====================================================
# 🔹 VOICE RECORDING ADMIN
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "note",
        "uploaded_by",
        "uploaded_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "note",
    )

    ordering = ("-uploaded_at",)

    readonly_fields = (
        "uploaded_at",
        "uploaded_by",
    )


# =====================================================
# 🔹 STAFF ADMIN
# =====================================================

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )