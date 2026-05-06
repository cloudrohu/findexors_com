from django.contrib import admin
from .models import (
    AhmedabadResponse,
    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,
    Staff,
    AhmedabadCompany,
    AhmedabadRealEstateGMB,
)

from utility.models import (
    Locality
)

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



from import_export.admin import ImportExportModelAdmin
from .resources import AhmedabadRealEstateGMBResource

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user",)

class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.created_by:
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        parent = form.instance  # AhmedabadResponse object

        for obj in instances:
            # USER AUTO SET
            if hasattr(obj, "created_by") and not obj.created_by:
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()

            # 🔥 MAIN LOGIC (IMPORTANT)
            if isinstance(obj, (Meeting, Followup)):
                if parent.status != "Deal_close":
                    parent.status = "Meeting_FollowUp"

                    # optional: deal done check
                    if getattr(obj, "status", None) == "Deal Done":
                        parent.status = "Deal_close"
                        parent.is_converted = True

                    parent.save()

        formset.save_m2m()


class CommentResponseInline(admin.StackedInline):
    model = Comment
    extra = 1
    fk_name = "response"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Response")
        super().save_model(request, obj, form, change)


class CommentCompanyInline(admin.StackedInline):
    model = Comment
    extra = 1
    fk_name = "company"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Company")
        super().save_model(request, obj, form, change)


class CommentRealestateGMBInline(admin.StackedInline):
    model = Comment
    extra = 1
    fk_name = "real_estate"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Real_Estate")
        super().save_model(request, obj, form, change)




class VoiceResponseInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    fk_name = "response"

    readonly_fields = ("uploaded_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Response")
        super().save_model(request, obj, form, change)


class VoiceCompanyInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    fk_name = "company"

    readonly_fields = ("uploaded_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Company")
        super().save_model(request, obj, form, change)


class VoiceRealestateGMBInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    fk_name = "real_estate"

    readonly_fields = ("uploaded_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Real_Estate")
        super().save_model(request, obj, form, change)




class VisitResponseInline(admin.StackedInline):
    model = Visit
    extra = 0
    fk_name = "response"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Response")
        super().save_model(request, obj, form, change)


class VisitCompanyInline(admin.StackedInline):
    model = Visit
    extra = 0
    fk_name = "company"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Company")
        super().save_model(request, obj, form, change)


class VisitRealestateGMBInline(admin.StackedInline):
    model = Visit
    extra = 0
    fk_name = "real_estate"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Real_Estate")
        super().save_model(request, obj, form, change)


class FollowupResponseInline(admin.StackedInline):
    model = Followup
    extra = 0
    fk_name = "response"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Response")
        super().save_model(request, obj, form, change)


class FollowupCompanyInline(admin.StackedInline):
    model = Followup
    extra = 0
    fk_name = "company"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Company")
        super().save_model(request, obj, form, change)


class FollowupRealestateGMBInline(admin.StackedInline):
    model = Followup
    extra = 0
    fk_name = "real_estate"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Real_Estate")
        super().save_model(request, obj, form, change)



class MeetingResponseInline(admin.StackedInline):
    model = Meeting
    extra = 0
    fk_name = "response"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Response")
        super().save_model(request, obj, form, change)


class MeetingCompanyInline(admin.StackedInline):
    model = Meeting
    extra = 0
    fk_name = "company"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Company")
        super().save_model(request, obj, form, change)


class MeetingRealestateGMBInline(admin.StackedInline):
    model = Meeting
    extra = 0
    fk_name = "real_estate"

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def save_model(self, request, obj, form, change):
        set_common_fields(obj, request, "Real_Estate")
        super().save_model(request, obj, form, change)










@admin.register(AhmedabadRealEstateGMB)
#class AhmedabadRealEstateGMBAdmin(ImportExportModelAdmin):
class AhmedabadRealEstateGMBAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/ahmedabad/ahmedabadrealestategmb/change_list.html"
    resource_class = AhmedabadRealEstateGMBResource
#class AhmedabadRealEstateGMBAdmin(admin.ModelAdmin):

    # 🔥 LIST VIEW (table columns)
    list_display = (
        "id",
        "name",
        "city_text",
        "phone",
        "status",
        "assigned_to",
        "rating",
        "reviews",
        "is_active",
        "created_at",
    )

    # 🔥 FILTERS (right sidebar)
    list_filter = (
        "status",
        "category",
        "city",
        "locality",
        'sub_locality',
        'postal_code',
        'business_status',
        "rating",
        "reviews",
        "updated_at",
        PhoneFilter,
    )

    # 🔥 SEARCH BAR
    search_fields = (
        "name",
        "phone",
        "city_text",
        "address",
        "place_id",
    )

    inlines = [
        CommentRealestateGMBInline,
        VoiceRealestateGMBInline,
        VisitRealestateGMBInline,
        FollowupRealestateGMBInline,
        MeetingRealestateGMBInline,
    ]
    # 🔥 SORTING
    ordering = ("-created_at",)

    # 🔥 CLICKABLE LINKS
    list_display_links = ("id", "name")

    # 🔥 FAST EDIT (inline editing)
    list_editable = (
        "status",
        "assigned_to",
        "is_active",
    )

    # 🔥 DATE FILTER (top)
    date_hierarchy = "created_at"

    # 🔥 PERFORMANCE OPTIMIZATION
    list_select_related = (
        "category",
        "city",
        "locality",
        "sub_locality",
        "assigned_to",
    )

    # 🔥 FORM LAYOUT (clean sections)
    fieldsets = (

        ("🏢 Basic Info", {
            "fields": (
                "name",
                "name_for_emails",
                "category",
                "type",
            )
        }),

        ("📍 Location", {
            "fields": (
                "city",
                "locality",
                "sub_locality",
                "address",
                "street",
                "city_text",
                "state",
                "postal_code",
                "country",
            )
        }),

        ("📞 Contact", {
            "fields": (
                "phone",
                "website",
            )
        }),

        ("📊 Google Data", {
            "fields": (
                "rating",
                "reviews",
                "place_id",
                "google_id",
                "cid",
                "business_status",
                "working_hours",
            )
        }),

        ("📝 Description", {
            "fields": (
                "description",
                "about",
                "logo",
            )
        }),

        ("⚙️ Status & Assignment", {
            "fields": (
                "status",
                "assigned_to",
                "is_active",
                "is_verified",
                "is_featured",
            )
        }),

        ("👤 Tracking", {
            "fields": (
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            )
        }),
    )

    # 🔥 READONLY FIELDS
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



# =====================================================
# ✅ COMPANY ADMIN (CARD UI)
# =====================================================
@admin.register(AhmedabadCompany)
class AhmedabadCompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    change_list_template = "admin/ahmedabad/company/card_list.html"
    list_per_page = 20
    preserve_filters = True

    inlines = [CommentCompanyInline,
               VoiceCompanyInline,
               VisitCompanyInline,
               FollowupCompanyInline,
               MeetingCompanyInline,
               ]

    list_display = (
        "id", "status", "company_name", "contact_no",
        "category", "locality", "assigned_to",
        "rating", "reviews_count", "updated_at",
    )

    search_fields = ("company_name", "contact_no", "email", "website", "address")

    list_filter = (
        "status", "category","locality",
        "assigned_to", "is_active", "is_verified", "is_featured",
    )

    readonly_fields = (
        "created_at", "updated_at",
        "created_by", "updated_by",
        "logo_preview",
    )

    ordering = ("-created_at",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "locality":
            kwargs["queryset"] = Locality.objects.filter(city__name="Ahmedabad")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# =======================
# MAIN ADMIN (NO TABS)
# =======================
@admin.register(AhmedabadResponse)
class AhmedabadResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    preserve_filters = True
    change_list_template = "admin/ahmedabad/ahmedabadresponse/change_list.html"

    list_display = (
        "id",
        "contact_no",
        "business_name",
        "status",
        'comment',
        "assigned_to",
        "is_converted",
        "create_at"
    )

    list_filter = ("status", "lead_source", "is_converted",)

    search_fields = ("contact_no", "business_name", "contact_persone")

    readonly_fields = ("created_by", "updated_by","create_at", "update_at", "converted_at")

    filter_horizontal = ("requirement_types",)

    # ✅ THIS IS IMPORTANT
    inlines = [
        CommentResponseInline,
        VoiceResponseInline,
        VisitResponseInline,
        FollowupResponseInline,
        MeetingResponseInline,
        
    ]

    fieldsets = (
        ("Basic Info", {
            "fields": ("contact_no", "contact_persone", "business_name", "status", "lead_source","locality","business_category", 'comment', "requirement_types","assigned_to",)
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "form_type",
        "response",
        "company",
        "comment",
        "create_at",
    )

    list_filter = ("form_type",)
    search_fields = ("comment",)

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    change_list_template = "admin/ahmedabad/voicerecording/change_form.html"


    list_display = (
        "id",
        "form_type",
        "response",
        "company",
        "uploaded_by",
        "create_at",
    )

    list_filter = ("form_type",)
    search_fields = ("file",)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "form_type",
        "response",
        "company",
        "visit_type",
        "visit_status",
        "created_by",   # ✅ FIXED
        "create_at",    # ✅ FIXED
    )

    list_filter = ("form_type", "visit_status", "visit_type")

    readonly_fields = (
        "created_by",   # ✅ FIXED
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "form_type",
        "response",
        "company",
        "status",
        "followup_date",
        "assigned_to",
        "created_by",
        "create_at",
    )

    list_filter = (
        "form_type",
        "status",
        "followup_date",
    )

    search_fields = (
        "response__business_name",
        "company__company_name",
        "assigned_to__name",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    change_list_template = "admin/ahmedabad/meeting/change_list.html"
    
    


    list_display = (
        "id",
        "form_type",
        "response",
        "company",
        "status",
        "meeting_date",
        "assigned_to",
        "created_by",
        "create_at",
    )

    list_filter = (
        "form_type",
        "status",
        "meeting_date",
    )

    search_fields = (
        "response__business_name",
        "company__company_name",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
