from django.contrib import admin
from django.db import models
from .models import Company, Comment, VoiceRecording, Visit, Followup, Meeting, Images, Faq


# =====================================================
# ✅ AUTO USER MIXIN
# =====================================================
class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not change:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# ✅ INLINE CLASSES
# =====================================================
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


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


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1
    max_num = 1


class ImageInline(admin.StackedInline):
    model = Images
    extra = 1


class FaqInline(admin.StackedInline):
    model = Faq
    extra = 1


# =====================================================
# ✅ COMPANY ADMIN
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    change_list_template = "admin/business/company_card_list.html"
    list_per_page = 200
    preserve_filters = True

    list_display = (
        "id",
        "status",
        "company_name",
        "contact_no",
        "category",
        "city",
        "locality",
        "assigned_to",
        "rating",
        "reviews_count",
        "updated_at",
    )

    search_fields = (
        "company_name",
        "contact_no",
        "email",
        "website",
        "address"
    )

    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        "assigned_to",
        "is_active",
        "is_verified",
        "is_featured",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "logo_preview"
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

    # 🔥 SMART SEARCH (C001 / PHONE)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            # C001 search
            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            # phone search
            if term.isdigit():
                queryset |= self.model.objects.filter(contact_no__icontains=term)

        return queryset, use_distinct