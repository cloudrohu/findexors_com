from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from urllib.parse import quote

from .models import Staff, Response, Meeting, Followup, Comment, VoiceRecording


# =====================================================
# ✅ AUTO USER MIXIN
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
# ✅ FILTER: Contact Status (Phone)
# =====================================================
class ContactFilter(admin.SimpleListFilter):
    title = "Contact"
    parameter_name = "contact_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Contact No"),
            ("no", "No Contact No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(contact_no__isnull=True).exclude(contact_no="")
        if self.value() == "no":
            return queryset.filter(models.Q(contact_no__isnull=True) | models.Q(contact_no=""))
        return queryset


# =====================================================
# ✅ RESPONSE INFO MIXIN (Inline show response data)
# =====================================================
class ResponseInfoMixin:
    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else "-"
    response_contact.short_description = "Contact"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else "-"
    response_business.short_description = "Business"

    def response_city(self, obj):
        return obj.response.city if obj.response else "-"
    response_city.short_description = "City"


# =====================================================
# ✅ INLINES (Inside Response)
# =====================================================
class MeetingInline(ResponseInfoMixin, admin.StackedInline):
    model = Meeting
    extra = 1
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class FollowupInline(ResponseInfoMixin, admin.StackedInline):
    model = Followup
    extra = 1
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class CommentInline(ResponseInfoMixin, admin.StackedInline):
    model = Comment
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceInline(ResponseInfoMixin, admin.StackedInline):
    model = VoiceRecording
    extra = 1
    readonly_fields = ("uploaded_at", "uploaded_by")


# =====================================================
# ✅ RESPONSE ADMIN (Main Card Like RealtyPMS)
# =====================================================
@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/response/response_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

    list_display = (
        "mr_id",
        "status",
        "lead_source",
        "contact_no",
        "whatsapp_status",
        "business_name",
        "business_category",
        "city",
        "assigned_to",
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
        "lead_source",
        "status",
        "business_category",
        "city",
        "locality",
        "assigned_to",
        ContactFilter,
        ("create_at", DateRangeFilter),
    )

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    fieldsets = (
        ("📞 Contact Info", {
            "fields": ("status", "assigned_to", "contact_no", "contact_persone")
        }),
        ("🏢 Business Details", {
            "fields": ("business_name", "business_category", "requirement_types", "city", "locality")
        }),
        ("📲 Lead Tracking", {
            "fields": ("lead_source", "whatsapp_welcome_sent")
        }),
        ("🕒 Audit", {
            "fields": ("create_at", "update_at", "created_by", "updated_by")
        }),
    )

    inlines = []

    def mr_id(self, obj):
        return f"MR{str(obj.id).zfill(3)}"
    mr_id.short_description = "Response ID"

    def whatsapp_status(self, obj):
        if getattr(obj, "whatsapp_welcome_sent", False):
            return format_html("<span style='color:green;font-weight:700;'>Sent</span>")
        return format_html("<span style='color:red;font-weight:700;'>Not Sent</span>")
    whatsapp_status.short_description = "WhatsApp"

# =====================================================
# ✅ MEETING ADMIN
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/response/meeting_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

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
        ("meeting_date", DateRangeFilter),
        ("create_at", DateRangeFilter),
        ("response__city", admin.RelatedOnlyFieldListFilter),
        ("response__locality", admin.RelatedOnlyFieldListFilter),
    )

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def mt_id(self, obj):
        return f"MT{str(obj.id).zfill(3)}"
    mt_id.short_description = "Meeting ID"

    # 🔥 MAGIC SEARCH (MT001 / MR001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("MT"):
                num = term.replace("MT", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("MR"):
                num = term.replace("MR", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(response__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ FOLLOWUP ADMIN
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/response/followup_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

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
        ("followup_date", DateRangeFilter),
        ("create_at", DateRangeFilter),
        ("response__city", admin.RelatedOnlyFieldListFilter),
        ("response__locality", admin.RelatedOnlyFieldListFilter),
    )

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def fu_id(self, obj):
        return f"FU{str(obj.id).zfill(3)}"
    fu_id.short_description = "Followup ID"

    # 🔥 MAGIC SEARCH (FU001 / MR001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("FU"):
                num = term.replace("FU", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("MR"):
                num = term.replace("MR", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(response__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/response/comment_card_list.html"
    list_per_page = 25
    ordering = ("-create_at",)

    list_display = ("cm_id", "response", "comment", "create_at", "created_by")
    search_fields = ("response__contact_no", "response__business_name", "comment")

    list_filter = (
        "response__status",
        "response__business_category",
        "response__city",
        "response__locality",
        ("create_at", DateRangeFilter),
    )

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")

    def cm_id(self, obj):
        return f"CM{str(obj.id).zfill(3)}"
    cm_id.short_description = "Comment ID"

    # 🔥 MAGIC SEARCH (CM001 / MR001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("CM"):
                num = term.replace("CM", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("MR"):
                num = term.replace("MR", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(response__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ VOICE RECORDING ADMIN
# =====================================================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/response/voice_card_list.html"
    list_per_page = 25
    ordering = ("-uploaded_at",)

    list_display = ("vr_id", "response", "file", "uploaded_by", "uploaded_at")
    search_fields = ("response__contact_no", "response__business_name")

    list_filter = (
        "response__status",
        "response__business_category",
        "response__city",
        "response__locality",
        ("uploaded_at", DateRangeFilter),
    )

    readonly_fields = ("uploaded_at", "uploaded_by")

    def vr_id(self, obj):
        return f"VR{str(obj.id).zfill(3)}"
    vr_id.short_description = "Recording ID"

    # 🔥 MAGIC SEARCH (VR001 / MR001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("VR"):
                num = term.replace("VR", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("MR"):
                num = term.replace("MR", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(response__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ STAFF ADMIN
# =====================================================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username", "user__first_name", "user__last_name")
