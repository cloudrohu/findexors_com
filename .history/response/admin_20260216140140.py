from django.contrib import admin
from .models import (
    Staff,
    Response,
    Meeting,
    Followup,
    Comment,
    VoiceRecording,
)


# ======================================================
# 🔹 INLINE MODELS
# ======================================================

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0
    show_change_link = True
    readonly_fields = ("create_at", "update_at")
    fields = (
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
        "create_at",
    )


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 0
    show_change_link = True
    readonly_fields = ("create_at", "update_at")
    fields = (
        "status",
        "followup_date",
        "assigned_to",
        "comment",
        "create_at",
    )


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("create_at", "update_at")
    fields = (
        "comment",
        "created_by",
        "create_at",
    )


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0
    readonly_fields = ("uploaded_at",)
    fields = (
        "file",
        "note",
        "uploaded_by",
        "uploaded_at",
    )


# ======================================================
# 🔹 STAFF ADMIN
# ======================================================

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    list_per_page = 30


# ======================================================
# 🔹 RESPONSE ADMIN (MAIN CRM)
# ======================================================

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "contact_no",
        "lead_source",
        "status",
        "assigned_to",
        "business_name",
        "city",
        "is_converted",
        "create_at",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "business_category",
        "city",
        "is_converted",
        "whatsapp_welcome_sent",
        "whatsapp_followup_1_sent",
        "whatsapp_followup_2_sent",
        "create_at",
    )

    search_fields = (
        "contact_no",
        "business_name",
        "contact_persone",
    )

    autocomplete_fields = (
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "created_by",
        "updated_by",
    )

    readonly_fields = (
        "create_at",
        "update_at",
        "converted_at",
    )

    date_hierarchy = "create_at"

    ordering = ("-create_at",)

    fieldsets = (
        ("Lead Info", {
            "fields": (
                "contact_no",
                "lead_source",
                "status",
                "assigned_to",
            )
        }),

        ("Business Info", {
            "fields": (
                "business_name",
                "contact_persone",
                "business_category",
                "requirement_types",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
            )
        }),

        ("WhatsApp Automation", {
            "fields": (
                "whatsapp_welcome_sent",
                "whatsapp_followup_1_sent",
                "whatsapp_followup_2_sent",
            )
        }),

        ("Conversion Tracking", {
            "fields": (
                "is_converted",
                "converted_at",
            )
        }),

        ("Meta", {
            "fields": (
                "created_by",
                "updated_by",
                "create_at",
                "update_at",
            )
        }),
    )

    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
    ]

    list_per_page = 30


# ======================================================
# 🔹 MEETING ADMIN
# ======================================================

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "status",
        "meeting_date",
        "assigned_to",
        "create_at",
    )

    list_filter = (
        "status",
        "assigned_to",
        "meeting_date",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
    )

    autocomplete_fields = (
        "response",
        "assigned_to",
    )

    date_hierarchy = "meeting_date"

    ordering = ("-meeting_date",)

    readonly_fields = (
        "create_at",
        "update_at",
    )


# ======================================================
# 🔹 FOLLOWUP ADMIN
# ======================================================

@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "response",
        "status",
        "followup_date",
        "assigned_to",
        "create_at",
    )

    list_filter = (
        "status",
        "assigned_to",
        "followup_date",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
    )

    autocomplete_fields = (
        "response",
        "assigned_to",
    )

    date_hierarchy = "followup_date"

    ordering = ("-followup_date",)

    readonly_fields = (
        "create_at",
        "update_at",
    )
