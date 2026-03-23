from django.contrib import admin
from .models import Company, Comment, VoiceRecording, Visit, Followup, Meeting, Images, Faq


# =====================================================
# ✅ AUTO USER MIXIN (MAIN + INLINE SUPPORT)
# =====================================================
class AutoUserAdminMixin:

    def save_model(self, request, obj, form, change):

        # created_by (only first time)
        if hasattr(obj, "created_by") and not change:
            if not obj.created_by:
                obj.created_by = request.user

        # updated_by (always)
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        # uploaded_by (file models)
        if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)

    # 🔥 INLINE AUTO USER
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:

            # created_by
            if hasattr(obj, "created_by") and not obj.pk:
                obj.created_by = request.user

            # updated_by
            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            # uploaded_by
            if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
                obj.uploaded_by = request.user

            obj.save()

        formset.save_m2m()


# =====================================================
# ✅ INLINE CLASSES (READONLY + AUTO)
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
# ✅ COMPANY ADMIN (FINAL CRM VERSION)
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

    # 🔥 ALL AUDIT FIELDS READONLY
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
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

    # 🔥 OPTIONAL FILTER SUPPORT (CUSTOM UI use karoge to)
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        status = request.GET.get("status")
        city = request.GET.get("city")
        assigned = request.GET.get("assigned_to")

        if status:
            qs = qs.filter(status=status)

        if city:
            qs = qs.filter(city_id=city)

        if assigned:
            qs = qs.filter(assigned_to_id=assigned)

        return qs