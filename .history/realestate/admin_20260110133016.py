from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db import models

from import_export.admin import ImportExportModelAdmin

from .models import (
    GoogleCompany,
    Company,
    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,

    # agar ye models tumhare app me hain to import rahenge
    Approx,
    SocialLink,
    Error,
    Images,
    Faq,
)


# =====================================================
# ✅ CUSTOM FILTER: Contact Number
# =====================================================
class ContactNumberFilter(admin.SimpleListFilter):
    title = "Contact Number"
    parameter_name = "contact_no_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Number"),
            ("no", "No Number"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(contact_no__isnull=True).exclude(contact_no="")
        if self.value() == "no":
            return queryset.filter(
                models.Q(contact_no__isnull=True) | models.Q(contact_no="")
            )
        return queryset


# =====================================================
# ✅ AUTO USER MIXIN
# =====================================================
class AutoUserAdminMixin:
    """
    Auto set:
    created_by / updated_by / uploaded_by
    """

    def save_model(self, request, obj, form, change):
        # created_by
        if hasattr(obj, "created_by") and not change and not getattr(obj, "created_by", None):
            obj.created_by = request.user

        # updated_by
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        # uploaded_by
        if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:
            if hasattr(obj, "created_by") and not getattr(obj, "created_by", None):
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            if hasattr(obj, "uploaded_by") and not getattr(obj, "uploaded_by", None):
                obj.uploaded_by = request.user

            obj.save()

        formset.save_m2m()


# =====================================================
# ✅ INLINE FORMSETS (No duplicate possible in OneToOne)
# =====================================================
class FollowupInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        return


class MeetingInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        return


# =====================================================
# ✅ INLINES
# =====================================================
class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by")


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 0
    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")


class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 0
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 0
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# ✅ GOOGLE COMPANY ADMIN (Outscraper)
# =====================================================
@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "category_text",
        "city_text",
        "state",
        "postal_code",
        "rating",
        "reviews",
        "business_status",
        "created_at",
    )
    search_fields = ("name", "phone", "place_id", "google_id", "cid")
    list_filter = ("business_status", "country", "state")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25


# =====================================================
# ✅ COMPANY ADMIN (Import/Export)
# =====================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, ImportExportModelAdmin):

    list_display = (
        "id",
        "company_name",
        "category",
        "city",
        "locality",
        "project",
        "contact_no",
        "status",
        "rating",
        "reviews_count",
        "is_verified",
        "is_featured",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        "project",
        "assigned_to",
        ContactNumberFilter,
    )

    search_fields = ("company_name", "contact_no")

    # ✅ C016 search
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            term = search_term.upper().strip()
            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

        return queryset, use_distinct

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "slug",
        "logo_preview",
    )

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "company_name",
                "contact_no",
                "email",
                "category",
                "city",
                "locality",
                "sub_locality",
                "project",
                "address",
                "description",
                "logo",
                "logo_preview",
            )
        }),
        ("⭐ Google / Rating", {
            "fields": (
                "rating",
                "reviews_count",
                "business_status_raw",
                "google_map",
                "googlemap_status",
                "website",
            )
        }),
        ("📊 Status & Assignment", {
            "fields": (
                "status",
                "assigned_to",
                "is_active",
                "is_verified",
                "is_featured",
            )
        }),
        ("🕒 Audit", {
            "fields": (
                "slug",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            )
        }),
    )

    inlines = [
        ImagesInline,
        SocialLinkInline,
        FaqInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline,
    ]

    list_per_page = 20


# =====================================================
# ✅ COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "company__contact_no", "comment")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# ✅ VOICE RECORDING ADMIN
# =====================================================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("uploaded_by", "uploaded_at")


# =====================================================
# ✅ VISIT ADMIN
# =====================================================
@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name", "company__contact_no")
    list_filter = ("visit_type", "visit_status", "company__city", "company__locality")
    readonly_fields = ("uploaded_by", "uploaded_at", "updated_at")


# =====================================================
# ✅ FOLLOWUP ADMIN (Company fields show)
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "company_name",
        "company_city",
        "company_locality",
        "company_contact",
        "company_category",
        "status",
        "followup_date",
        "assigned_to",
        "created_by",
        "update_at",
    )

    list_filter = (
        "status",
        "assigned_to",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    # ✅ Search: C016 / F002 / number
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.startswith("F"):
                num = term.replace("F", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__contact_no__icontains=term)

        return queryset, use_distinct

    # ===== Company fields =====
    def company_name(self, obj):
        return obj.company.company_name
    company_name.short_description = "Company"

    def company_city(self, obj):
        return obj.company.city
    company_city.short_description = "City"

    def company_locality(self, obj):
        return obj.company.locality
    company_locality.short_description = "Locality"

    def company_contact(self, obj):
        return obj.company.contact_no
    company_contact.short_description = "Contact"

    def company_category(self, obj):
        return obj.company.category
    company_category.short_description = "Category"


# =====================================================
# ✅ MEETING ADMIN (Company fields show)
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    list_display = (
        "id",
        "company_name",
        "company_city",
        "company_locality",
        "company_contact",
        "company_category",
        "status",
        "meeting_date",
        "assigned_to",
        "created_by",
        "update_at",
    )

    list_filter = (
        "status",
        "assigned_to",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    # ✅ Search: C016 / M002 / number
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.startswith("M"):
                num = term.replace("M", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__contact_no__icontains=term)

        return queryset, use_distinct

    # ===== Company fields =====
    def company_name(self, obj):
        return obj.company.company_name
    company_name.short_description = "Company"

    def company_city(self, obj):
        return obj.company.city
    company_city.short_description = "City"

    def company_locality(self, obj):
        return obj.company.locality
    company_locality.short_description = "Locality"

    def company_contact(self, obj):
        return obj.company.contact_no
    company_contact.short_description = "Contact"

    def company_category(self, obj):
        return obj.company.category
    company_category.short_description = "Category"
