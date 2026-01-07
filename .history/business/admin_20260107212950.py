from django.contrib import admin
from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils import translation
if not hasattr(translation, "ugettext_lazy"):
    translation.ugettext_lazy = translation.gettext_lazy
from tabbed_admin import TabbedModelAdmin  # Ab ye line error nahi degi



class AutoAuditAdminMixin:
    """
    Auto set created_by / updated_by
    Audit fields readonly
    """

    readonly_fields = (
        "create_at",
        "update_at",
        "created_by",
        "updated_by",
    )

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.created_by:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if hasattr(obj, "created_by") and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user
            obj.save()
        formset.save_m2m()



# =====================================================
# AUTO USER MIXIN
# =====================================================
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
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user
            obj.save()
        formset.save_m2m()


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
            raise ValidationError(
                "❌ Ek company ke liye sirf 1 Active Followup allowed hai."
            )



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
            raise ValidationError(
                "❌ Ek company ke liye sirf 1 Active Meeting allowed hai."
            )


# =====================================================
# INLINE MODELS
# =====================================================
class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0
    exclude = ("created_by", "updated_by", "create_at", "update_at")


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")



class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    classes = ("tab-6-comments",)



class VoiceRecordingInline(admin.StackedInline):
    model = VoiceRecording
    extra = 1
    classes = ("tab-4-voice-recordings",)
    exclude = ("created_by", "updated_by", "create_at", "update_at")



class VisitInline(admin.StackedInline):
    model = Visit
    extra = 1
    classes = ("tab-5-visits",)
    exclude = ("created_by", "updated_by", "create_at", "update_at")





class FollowupInline(admin.StackedInline):   # 🔥 CHANGED
    model = Followup
    formset = FollowupInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")
    classes = ("tab-3-followups",)



class MeetingInline(admin.StackedInline):   # 🔥 CHANGED
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")
    classes = ("tab-2-meetings",)



# =====================================================
# COMPANY ADMIN
# =====================================================


# Agar aap 'django-tabbed-admin' use kar rahe hain to ye import karein:
# from tabbed_admin import TabbedModelAdmin 
# Agar library nahi hai to pip install django-tabbed-admin karein aur settings me add karein.

# Filhal main standard ModelAdmin ke sath structure sahi kar raha hu, 
# lekin Tabs chalane ke liye aapko TabbedModelAdmin ki zarurat padegi.

@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin): # 🔥 AutoUserAdminMixin Add kiya

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'js/admin_dependent_dropdown.js',
        )
    list_display = (
        "id",
        "company_name",
        "category",
        "city",
        "locality",
        "sub_locality",
        "project",
        "contact_no",
        "status",
        "is_verified",
        "is_featured",
        "assigned_to",
        "created_by",     # ✅ OK
        "updated_by",     # ✅ OK
        "created_at",     # ✅ FIXED
        "updated_at",     # ✅ FIXED
    )


    list_filter = (
        "status", "category",
        "city", "locality", "sub_locality", "project",
        "is_verified", "is_featured",
        "assigned_to"
    )

    search_fields = ("company_name", "contact_no")

    readonly_fields = ("slug", "created_at", "updated_at", "logo_preview")

    # Fieldsets sirf Company ke fields ke liye rakhein
    fieldsets = (
        ("🏢 Company Info", {
            "fields": (
                 "status","assigned_to","company_name", "contact_no", "whatsapp", "email", "category",
                "city", "locality", "sub_locality", "project",
                "address", "description",
                "logo", "logo_preview"
            )
        }),
        ("📊 Status & Assignment", {
            "fields": (
                "is_active", "is_verified", "is_featured","website", "google_map"
            )
        }),
        ("🕒 Audit Info", {"fields": ("slug","created_at", "updated_at")}),
    )

    inlines = [
        ImagesInline,
        SocialLinkInline,
        FaqInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
        FollowupInline,
        MeetingInline
    ]

    # 🔥 MAIN FIX: Strings ki jagah Inline Classes ka use karein
    tabs = [
        ("Company Info", (
            "company_name", "contact_no", "category", "city", "locality", "address"
        )),
        ("4. Voice Recordings", (VoiceRecordingInline,)),  # ✅ String hatakar Class likha
        ("5. Visits", (VisitInline,)),                     # ✅ Sahi tarika
        ("3. Followups", (FollowupInline,)),               # ✅ Sahi tarika
        ("2. Meetings", (MeetingInline,)),                 # ✅ Sahi tarika
        ("6. Comments", (CommentInline,)),                 # ✅ Sahi tarika
    ]

    list_per_page = 20


# =====================================================
# OTHER ADMINS
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


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
        "company__city",
        "company__category",
    )

    search_fields = (
        "company__company_name",
        "company__contact_no",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    # ======================
    # Company related fields
    # ======================

    def company_name(self, obj):
        return obj.company.company_name
    company_name.short_description = "Company Name"
    company_name.admin_order_field = "company__company_name"

    def company_city(self, obj):
        return obj.company.city
    company_city.short_description = "City"
    company_city.admin_order_field = "company__city"

    def company_locality(self, obj):
        return obj.company.locality
    company_locality.short_description = "Locality"
    company_locality.admin_order_field = "company__locality"

    def company_contact(self, obj):
        return obj.company.contact_no
    company_contact.short_description = "Contact No"

    def company_category(self, obj):
        return obj.company.category
    company_category.short_description = "Category"

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

    list_filter = ("status", "assigned_to", "company__city","company__locality", "company__category")
    search_fields = ("company__company_name", "company__contact_no")

    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    # ======================
    # Company related fields
    # ======================

    def company_name(self, obj):
        return obj.company.company_name
    company_name.short_description = "Company Name"
    company_name.admin_order_field = "company__company_name"

    def company_city(self, obj):
        return obj.company.city
    company_city.short_description = "City"
    company_city.admin_order_field = "company__city"

    def company_locality(self, obj):
        return obj.company.locality
    company_locality.short_description = "Locality"
    company_locality.admin_order_field = "company__locality"

    def company_contact(self, obj):
        return obj.company.contact_no
    company_contact.short_description = "Contact No"

    def company_category(self, obj):
        return obj.company.category
    company_category.short_description = "Category"


@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )