from django.contrib import admin
from .models import (
    Company, Images, Comment,
    VoiceRecording, Visit, Faq
)


# =====================================================
# INLINE
# =====================================================
class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 0


# =====================================================
# COMPANY ADMIN
# =====================================================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "id", "company_name", "category",
        "city", "locality",
        "status", "is_verified",
        "created_at"
    )

    search_fields = ("company_name", "contact_no")
    list_filter = ("status", "category", "city")

    readonly_fields = ("slug", "logo_preview", "created_at", "updated_at")

    fieldsets = (
        ("Company Info", {
            "fields": (
                "company_name", "category",
                "city", "locality", "sub_locality",
                "address", "description",
                "logo", "logo_preview"
            )
        }),
        ("Contact", {
            "fields": ("contact_no", "whatsapp", "email", "website")
        }),
        ("Status", {
            "fields": ("status", "assigned_to", "is_active", "is_verified", "is_featured")
        }),
        ("SEO", {"fields": ("slug",)}),
        ("Audit", {"fields": ("created_at", "updated_at")}),
    )

    inlines = [
        ImagesInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FaqInline,
    ]


# =====================================================
# OTHER ADMINS
# =====================================================
@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "uploaded_by", "uploaded_at")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "question")
