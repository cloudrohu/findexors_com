from django.contrib import admin
from django.db import models
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


# =====================================================
# 🔹 MAGIC SEARCH MIXIN
# =====================================================

class MagicSearchMixin:
    prefix_map = {}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if not search_term:
            return queryset, use_distinct

        term = search_term.upper().strip()

        for prefix, field in self.prefix_map.items():
            if term.startswith(prefix):
                num = term.replace(prefix, "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(**{field: int(num)})

        if term.isdigit():
            if hasattr(self.model, "response"):
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)
            elif hasattr(self.model, "contact_no"):
                queryset |= self.model.objects.filter(contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# 🔹 RESPONSE ADMIN (CARD VIEW READY)
# =====================================================

@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    change_list_template = "admin/response/response_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

    prefix_map = {"MR": "id"}

    list_display = (
        "mr_id",
        "status",
        "lead_source",
        "contact_no",
        "business_name",
        "business_category",
        "city",
        "locality",
        "assigned_to",
        "is_converted",
        "create_at",
    )

    search_fields = (
        "contact_no",
        "business_name",
        "contact_persone",
        "city__name",
        "locality__name",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "is_converted",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
        "converted_at",
    )

    date_hierarchy = "create_at"

    fieldsets = (
        ("📞 Contact Info", {
            "fields": ("status", "assigned_to", "contact_no", "contact_persone")
        }),
        ("🏢 Business Details", {
            "fields": ("business_name", "business_category", "requirement_types", "city", "locality")
        }),
        ("📲 Lead Tracking", {
            "fields": (
                "lead_source",
                "whatsapp_welcome_sent",
                "whatsapp_followup_1_sent",
                "whatsapp_followup_2_sent",
            )
        }),
        ("💰 Conversion", {
            "fields": ("is_converted", "converted_at")
        }),
        ("🕒 Audit", {
            "fields": ("create_at", "update_at", "created_by", "updated_by")
        }),
    )

    def mr_id(self, obj):
        return f"MR{str(obj.id).zfill(3)}"
    mr_id.short_description = "Response ID"


# =====================================================
# 🔹 MEETING ADMIN
# =====================================================

@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    change_list_template = "admin/response/meeting_card_list.html"
    list_per_page = 25
    ordering = ("-meeting_date",)

    prefix_map = {
        "MT": "id",
        "MR": "response__id",
    }

    list_display = (
        "mt_id",
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
        "response__city",
        "response__locality",
        "response__business_category",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def mt_id(self, obj):
        return f"MT{str(obj.id).zfill(3)}"
    mt_id.short_description = "Meeting ID"


# =====================================================
# 🔹 FOLLOWUP ADMIN
# =====================================================

@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    change_list_template = "admin/response/followup_card_list.html"
    list_per_page = 25
    ordering = ("-followup_date",)

    prefix_map = {
        "FU": "id",
        "MR": "response__id",
    }

    list_display = (
        "fu_id",
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
        "response__city",
        "response__locality",
        "response__business_category",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def fu_id(self, obj):
        return f"FU{str(obj.id).zfill(3)}"
    fu_id.short_description = "Followup ID"


# =====================================================
# 🔹 COMMENT ADMIN
# =====================================================

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    change_list_template = "admin/response/comment_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

    prefix_map = {
        "CM": "id",
        "MR": "response__id",
    }

    list_display = (
        "cm_id",
        "response",
        "create_at",
        "created_by",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "response__status",
        "response__business_category",
        "response__city",
        "response__locality",
    )

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
    )

    def cm_id(self, obj):
        return f"CM{str(obj.id).zfill(3)}"
    cm_id.short_description = "Comment ID"


# =====================================================
# 🔹 VOICE RECORDING ADMIN
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    change_list_template = "admin/response/voice_card_list.html"
    list_per_page = 25
    ordering = ("-uploaded_at",)

    prefix_map = {
        "VR": "id",
        "MR": "response__id",
    }

    list_display = (
        "vr_id",
        "response",
        "uploaded_by",
        "uploaded_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
    )

    list_filter = (
        "response__status",
        "response__business_category",
        "response__city",
        "response__locality",
    )

    readonly_fields = (
        "uploaded_at",
        "uploaded_by",
    )

    def vr_id(self, obj):
        return f"VR{str(obj.id).zfill(3)}"
    vr_id.short_description = "Recording ID"


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
