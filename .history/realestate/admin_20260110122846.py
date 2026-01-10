from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from import_export.admin import ImportExportModelAdmin

from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

# =====================================================
# AUTO USER MIXIN
# =====================================================
from django.db import models


from django.contrib import admin

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


class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not change and not obj.created_by:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
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
# FORMSET VALIDATIONS
# =====================================================

class FollowupInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("status") in ["New Followup", "Re Followup"]:
                active += 1
        if active > 1:
            raise ValidationError("❌ Sirf 1 Active Followup allowed hai")


class MeetingInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("status") in ["New Meeting", "Re Meeting"]:
                active += 1
        if active > 1:
            raise ValidationError("❌ Sirf 1 Active Meeting allowed hai")


# =====================================================
# INLINES
# =====================================================

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1


class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1


class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


# =====================================================
# COMPANY ADMIN (MAIN)
# =====================================================

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, ImportExportModelAdmin):

    resource_class = CompanyResource
    """
    ✅ Search (C016 / phone / name)
    ✅ Import / Export ready
    ✅ Audit readonly
    ✅ Clean fieldsets
    """

    # =========================
    # LIST VIEW
    # =========================
    list_display = (
        "id",
        "company_name",
        "category",
        "city",
        "locality",
        "address",
        "project",
        "contact_no",
        "status",
        "is_verified",
        "is_featured",
        "assigned_to",
        "created_at",
    )

    list_per_page = 20

    # =========================
    # SEARCH
    # =========================
    search_fields = (
        "company_name",
        "contact_no",
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        # 🔥 Allow search like: C016 / c016
        if search_term:
            term = search_term.upper().strip()

            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

        return queryset, use_distinct

    # =========================
    # FILTERS
    # =========================
    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        "project",
        ContactNumberFilter,
    )

    # =========================
    # READONLY (AUDIT SAFE)
    # =========================
    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "logo_preview",
        "slug",
    )

    # =========================
    # FORM LAYOUT
    # =========================
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
        ("📊 Status & Assignment", {
            "fields": (
                "status",
                "assigned_to",
                "is_active",
                "is_verified",
                "is_featured",
                "website",
                "google_map",
            )
        }),
        ("🕒 Audit Info", {
            "fields": (
                "slug",
                "created_at",
                "updated_at",
            )
        }),
    )

    # =========================
    # INLINE MODELS
    # =========================
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
# OTHER ADMINS
# =====================================================

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
    )


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by")
    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
        "updated_at",
    )


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    change_list_template = "admin/business/company/followup_card_list.html"

    list_display = (
        "id",
        "company",
        "status",
        "followup_date",
        "assigned_to",
        "created_by",
    )

    # 🔍 BASIC SEARCH
    search_fields = (
        "company__company_name",
        "company__contact_no",
    )

    # 🎛 COMPANY-LIKE FILTERS
    list_filter = (
        "status",
        "assigned_to",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    # 🔥 ADVANCED SEARCH (C001 / F001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            term = search_term.upper().strip()

            # 👉 COMPANY ID SEARCH (C016)
            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(
                        company__id=int(num)
                    )

            # 👉 FOLLOWUP ID SEARCH (F004)
            if term.startswith("F"):
                num = term.replace("F", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(
                        id=int(num)
                    )

            # 👉 NUMBER SEARCH (CONTACT)
            if term.isdigit():
                queryset |= self.model.objects.filter(
                    company__contact_no__icontains=term
                )

        return queryset, use_distinct

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")




@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    change_list_template = "admin/business/company/meeting_card_list.html"

    list_display = (
        "id",
        "company",
        "status",
        "meeting_date",
        "assigned_to",
        "created_by",
    )

    # 🔍 BASIC SEARCH (name + number)
    search_fields = (
        "company__company_name",
        "company__contact_no",
    )

    # 🎛 ALL COMPANY-LIKE FILTERS
    list_filter = (
        "status",
        "assigned_to",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    # 🔥 MAGIC SEARCH LOGIC (C001 / M001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            term = search_term.upper().strip()

            # 👉 COMPANY ID SEARCH (C016)
            if term.startswith("C"):
                num = term.replace("C", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(
                        company__id=int(num)
                    )

            # 👉 MEETING ID SEARCH (M005)
            if term.startswith("M"):
                num = term.replace("M", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(
                        id=int(num)
                    )

            # 👉 PURE NUMBER (CONTACT / ID)
            if term.isdigit():
                queryset |= self.model.objects.filter(
                    company__contact_no__icontains=term
                )

        return queryset, use_distinct
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")
    





@admin.register(Approx)
class ApproxAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")
    readonly_fields = (
        "create_at",
        "update_at",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")
    readonly_fields = (
        "create_at",
        "update_at",
    )


@admin.register(Error)
class ErrorAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")


@admin.register(Images)
class ImagesAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")


@admin.register(Faq)
class FaqAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    readonly_fields = (
        "create_at",
        "update_at",
    )







