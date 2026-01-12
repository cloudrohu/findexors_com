from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin

from .models import GoogleCompany, Comment, VoiceRecording, Visit, Followup, Meeting
from .resources import GoogleCompanyResource

from django.contrib import admin
from import_export.admin import ImportExportMixin # ✅ ImportExportModelAdmin ki jagah Mixin layein
# ... baaki imports ...

# =====================================================
# ✅ FILTER: Phone Status
# =====================================================
class PhoneFilter(admin.SimpleListFilter):
    title = "Phone"
    parameter_name = "phone_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Phone"),
            ("no", "No Phone"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(phone__isnull=True).exclude(phone="")
        if self.value() == "no":
            return queryset.filter(models.Q(phone__isnull=True) | models.Q(phone=""))
        return queryset


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
# ✅ INLINES (Inside GoogleCompany)
# =====================================================
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")


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
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 1
    max_num = 1
    can_delete = True
    exclude = ("created_by", "updated_by", "create_at", "update_at")


from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import GoogleCompany
from .resources import GoogleCompanyResource

# ... Baki imports aur filters wese hi rahenge ...

@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportMixin, admin.ModelAdmin): # ✅ Notice: Mixin pehle, ModelAdmin baad me
    resource_class = GoogleCompanyResource
    
    # ✅ Variable ki jagah Method use karein
    def get_changelist_template(self, request):
        return "admin/realestate/googlecompany/change_list.html"

    list_display = (
        "id", "status", "name", "phone", "category",
        "city", "locality", "project", "rating", "reviews", "updated_at",
    )
    
    search_fields = ("name", "phone", "place_id", "google_id", "cid", "address")
    
    list_filter = (
        "status", "category", "city", "locality", 
        "sub_locality", "project", "business_status",
    )

    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "updated_by", "created_by")
    list_per_page = 25

    # ... Baki fieldsets aur inlines wese hi rakhein ...

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "Google Companies Card View" # Title change karke check karein
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportMixin, admin.ModelAdmin): # ✅ Yahan change karein
    resource_class = GoogleCompanyResource
    change_list_template = "admin/realestate/googlecompany/change_list.html"


    list_display = (
        "id",
        "status",
        "name",
        "phone",
        "category",
        "city",
        "locality",
        "project",
        "rating",
        "reviews",
        "updated_at",
    )

    search_fields = ("name", "phone", "place_id", "google_id", "cid", "address")

    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        "sub_locality",
        "project",
        "business_status",
        PhoneFilter,
    )

    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "updated_by", "created_by")
    list_per_page = 25

    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                "status", "category",
                "city", "sub_locality", "locality",
                "project",
                "name", "type",
                "phone", "website",
                "address", "street",
                "postal_code",
                "country",
            )
        }),
        ("⭐ Google Stats", {
            "fields": (
                "rating", "reviews",
                "business_status", "working_hours",
            )
        }),
        ("🔎 IDs", {
            "fields": ("place_id", "google_id", "cid")
        }),
        ("📍 Geo", {
            "fields": ("latitude", "longitude")
        }),
        ("🕒 Audit", {
            "fields": ("created_at", "updated_at", "created_by", "updated_by")
        }),
    )

    inlines = [CommentInline, VoiceInline, VisitInline, FollowupInline, MeetingInline]

    # 🔥 MAGIC SEARCH LOGIC (G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            # 👉 COMPANY ID SEARCH (G016)
            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            # 👉 PURE NUMBER => Phone search
            if term.isdigit():
                queryset |= self.model.objects.filter(phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ COMMENT ADMIN (Card + Search Like Business)
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/realestate/googlecompany/comment_card_list.html"

    list_display = ("id", "company", "comment", "create_at", "created_by")
    search_fields = ("company__name", "company__phone", "comment")

    list_filter = (
        "company__status",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")

    # 🔥 MAGIC SEARCH LOGIC (CM001 / G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("CM"):
                num = term.replace("CM", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ VOICE ADMIN
# =====================================================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/realestate/googlecompany/voice_card_list.html"

    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")

    list_filter = (
        "company__status",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = ("uploaded_at", "uploaded_by")

    # 🔥 MAGIC SEARCH (R001 / G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("R"):
                num = term.replace("R", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ VISIT ADMIN
# =====================================================
@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/realestate/googlecompany/visit_card_list.html"

    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    search_fields = ("company__name", "company__phone")

    list_filter = (
        "visit_type",
        "visit_status",
        "company__status",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = ("uploaded_at", "uploaded_by", "updated_at")

    # 🔥 MAGIC SEARCH (V001 / G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("V"):
                num = term.replace("V", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ FOLLOWUP ADMIN
# =====================================================
@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/realestate/googlecompany/followup_card_list.html"

    list_display = ("id", "company", "status", "followup_date", "assigned_to", "update_at")
    search_fields = ("company__name", "company__phone")

    list_filter = (
        "status",
        "assigned_to",
        "company__status",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = ("create_at", "update_at", "created_by", "updated_by")

    # 🔥 MAGIC SEARCH (F001 / G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("F"):
                num = term.replace("F", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# ✅ MEETING ADMIN (Business Style)
# =====================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/realestate/googlecompany/meeting_card_list.html"

    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "created_by")
    search_fields = ("company__name", "company__phone")

    list_filter = (
        "status",
        "assigned_to",
        "company__category",
        "company__city",
        "company__locality",
        "company__project",
    )

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    # 🔥 MAGIC SEARCH LOGIC (M001 / G001)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("M"):
                num = term.replace("M", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("G"):
                num = term.replace("G", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(company__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(company__phone__icontains=term)

        return queryset, use_distinct
