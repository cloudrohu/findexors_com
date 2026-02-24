from django.contrib import admin
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
# 🔹 INLINE CLASSES
# =====================================================

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    show_change_link = True


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    show_change_link = True


from django.utils.html import format_html
from django.contrib import admin

# =====================================================
# 🔹 RESPONSE ADMIN (PRO VERSION)
# =====================================================

@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"MR": "id"}

    # ✅ INLINE SECTION
    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
    ]

    list_display = (
        "mr_id",
        "colored_status",
        "lead_source",
        "contact_no",
        "contact_persone",
        "business_name",
        "city",
        "assigned_to",
        "converted_badge",
        "create_at",
    )

    list_display_links = ("mr_id", "contact_persone", "business_name")

    search_fields = (
        "contact_no",
        "contact_persone",
        "business_name",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "is_converted",
        "create_at",
    )

    ordering = ("-create_at",)
    date_hierarchy = "create_at"

    list_select_related = (
        "assigned_to",
        "business_category",
        "city",
        "locality",
    )

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")

    fieldsets = (
        ("Business Details", {
            "fields": (
                "business_name",
                "business_category",
                "contact_persone",
                "contact_no",
            )
        }),
        ("Lead Information", {
            "fields": (
                "status",
                "lead_source",
                "assigned_to",
                "is_converted",
            )
        }),
        
        ("Location Details", {
            "fields": (
                "city",
                "locality",
            )
        }),
        ("System Information", {
            "fields": (
                "created_by",
                "updated_by",
                "create_at",
                "update_at",
            ),
            "classes": ("collapse",),
        }),
    )

    # ==============================
    # 🔹 Custom Display Methods
    # ==============================

    def mr_id(self, obj):
        return format_html(
            "<b style='color:#2563eb;'>MR{}</b>",
            str(obj.id).zfill(3)
        )
    mr_id.short_description = "Response ID"

    def converted_badge(self, obj):
        if obj.is_converted:
            return format_html(
                "<span style='color:white;background:green;padding:4px 8px;border-radius:6px;'>Converted</span>"
            )
        return format_html(
            "<span style='color:white;background:red;padding:4px 8px;border-radius:6px;'>Pending</span>"
        )
    converted_badge.short_description = "Conversion"

    def colored_status(self, obj):
        color = "gray"

        if obj.status == "new":
            color = "#2563eb"
        elif obj.status == "followup":
            color = "#f59e0b"
        elif obj.status == "closed":
            color = "#16a34a"
        elif obj.status == "rejected":
            color = "#dc2626"

        return format_html(
            "<b style='color:{};'>{}</b>",
            color,
            obj.status.upper()
        )

    colored_status.short_description = "Status"


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"MT": "id", "MR": "response__id"}

    list_display = (
        "mt_id",
        "response",
        "status",
        "meeting_date",
        "assigned_to",
        "create_at",
        "update_at",
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
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
    )

    ordering = ("-meeting_date",)

    list_select_related = ("response", "assigned_to")

    def mt_id(self, obj):
        return f"MT{str(obj.id).zfill(3)}"
    mt_id.short_description = "Meeting ID"

# =====================================================
# 🔹 FOLLOWUP ADMIN
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"FU": "id", "MR": "response__id"}

    list_display = (
        "fu_id",
        "response",
        "status",
        "followup_date",
        "assigned_to",
        "create_at",
        "update_at",
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
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
    )

    ordering = ("-followup_date",)

    list_select_related = ("response", "assigned_to")

    def fu_id(self, obj):
        return f"FU{str(obj.id).zfill(3)}"
    fu_id.short_description = "Followup ID"
# =====================================================
# 🔹 COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"CM": "id", "MR": "response__id"}

    list_display = (
        "cm_id",
        "response",
        "comment",
        "created_by",
        "create_at",
        "update_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "create_at",
    )

    ordering = ("-create_at",)

    list_select_related = ("response",)

    def cm_id(self, obj):
        return f"CM{str(obj.id).zfill(3)}"

    cm_id.short_description = "Comment ID"
# =====================================================
# 🔹 VOICE RECORDING ADMIN
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"VR": "id", "MR": "response__id"}

    list_display = (
        "vr_id",
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

    list_filter = (
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "uploaded_at",
    )

    ordering = ("-uploaded_at",)

    list_select_related = ("response",)

    def vr_id(self, obj):
        return f"VR{str(obj.id).zfill(3)}"

    vr_id.short_description = "Recording ID"# =====================================================
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