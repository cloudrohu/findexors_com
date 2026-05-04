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
# AUTO USER MIXIN (IMPORTANT)
# =======================
class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.created_by:
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

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


# =======================
# INLINE MODELS (FIXED)
# =======================

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1   # ✅ important
    fields = ("comment",)
    classes = ("collapse",)


class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    fields = ("file",)
    readonly_fields = ("uploaded_at",)
    classes = ("collapse",)


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1
    fields = ("visit_for", "visit_type", "visit_status", "comment")
    readonly_fields = ("uploaded_at",)
    classes = ("collapse",)


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 1   # ✅ FIXED
    can_delete = True
    fields = ("status", "followup_date", "assigned_to", "comment")
    classes = ("collapse",)


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1   # ✅ FIXED
    can_delete = True
    fields = ("status", "meeting_date", "assigned_to", "comment")
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
class AhmedabadResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):

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

    # ✅ INLINE ENABLED
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