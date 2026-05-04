from django.contrib import admin
from .models import (
    AhmedabadResponse,
    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,
    Staff
)


# =======================
# INLINE MODELS
# =======================

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("create_at", "update_at")
    fields = ("comment", "created_by", "create_at")
    classes = ("collapse",)


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    readonly_fields = ("uploaded_at",)
    classes = ("collapse",)


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1
    readonly_fields = ("uploaded_at",)
    classes = ("collapse",)


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 0
    classes = ("collapse",)


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 0
    classes = ("collapse",)


# =======================
# STAFF ADMIN
# =======================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


# =======================
# MAIN CRM ADMIN
# =======================
@admin.register(AhmedabadResponse)
class AhmedabadResponseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "contact_no",
        "business_name",
        "status",
        "assigned_to",
        "is_converted",
        "create_at"
    )

    list_filter = (
        "status",
        "lead_source",
        "is_converted",
        "city"
    )

    search_fields = (
        "contact_no",
        "business_name",
        "contact_persone"
    )

    readonly_fields = (
        "create_at",
        "update_at",
        "converted_at"
    )

    filter_horizontal = ("requirement_types",)

    inlines = [
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline
    ]

    fieldsets = (
        ("📌 Basic Info", {
            "fields": (
                "contact_no",
                "contact_persone",
                "business_name",
                "status",
                "lead_source"
            )
        }),

        ("📍 Location", {
            "fields": ("city", "locality")
        }),

        ("📊 Business", {
            "fields": ("business_category", "requirement_types")
        }),

        ("👤 Assignment", {
            "fields": ("assigned_to",)
        }),

        ("📲 WhatsApp Tracking", {
            "classes": ("collapse",),
            "fields": (
                "whatsapp_welcome_sent",
                "whatsapp_followup_1_sent",
                "whatsapp_followup_2_sent"
            )
        }),

        ("💰 Conversion", {
            "fields": ("is_converted", "converted_at")
        }),

        ("⚙️ System Info", {
            "classes": ("collapse",),
            "fields": (
                "created_by",
                "updated_by",
                "create_at",
                "update_at"
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# =======================
# COMMENT ADMIN
# =======================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("comment",)
    list_filter = ("create_at",)


# =======================
# VOICE ADMIN
# =======================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)


# =======================
# VISIT ADMIN
# =======================
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by")
    list_filter = ("visit_status", "visit_type")


# =======================
# FOLLOWUP ADMIN
# =======================
@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "assigned_to", "followup_date")
    list_filter = ("status",)


# =======================
# MEETING ADMIN
# =======================
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "assigned_to", "meeting_date")
    list_filter = ("status",)