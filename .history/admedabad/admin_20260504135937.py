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
# AUTO USER MIXIN
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
# INLINE MODELS (WORKING)
# =======================

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    readonly_fields = ("created_by", "updated_by","create_at", "update_at",)



class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    readonly_fields = ("created_by", "updated_by","create_at", "update_at",)



class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1
    readonly_fields = ("created_by", "updated_by","create_at", "update_at",)


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 1
    readonly_fields = ("created_by", "updated_by","create_at", "update_at",)


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1
    readonly_fields = ("created_by", "updated_by","create_at", "update_at")


# =======================
# STAFF ADMIN
# =======================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user",)


# =======================
# MAIN ADMIN (NO TABS)
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

    list_filter = ("status", "lead_source", "is_converted", "city")

    search_fields = ("contact_no", "business_name", "contact_persone")

    readonly_fields = ("created_by", "updated_by","create_at", "update_at", "converted_at")

    filter_horizontal = ("requirement_types",)

    # ✅ THIS IS IMPORTANT
    inlines = [
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline
    ]

    fieldsets = (
        ("Basic Info", {
            "fields": ("contact_no", "contact_persone", "business_name", "status", "lead_source","locality","business_category", "requirement_types","assigned_to",)
        }),

        ("WhatsApp Tracking", {
            "fields": (
                "whatsapp_welcome_sent",
                "whatsapp_followup_1_sent",
                "whatsapp_followup_2_sent"
            )
        }),
        ("Conversion", {
            "fields": ("is_converted", "converted_at")
        }),
        ("System Info", {
            "fields": ("created_by", "updated_by", "create_at", "update_at")
        }),
    )