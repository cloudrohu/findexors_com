# ==========================================
# 1. FIX FOR DJANGO 4.0+ & TABBED ADMIN
# ==========================================
# Ye code sabse upar hona chahiye imports se pehle
from django.utils import translation
if not hasattr(translation, "ugettext_lazy"):
    translation.ugettext_lazy = translation.gettext_lazy

# ==========================================
# 2. IMPORTS
# ==========================================
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

# Tabbed Admin Import
try:
    from tabbed_admin import TabbedModelAdmin
except ImportError:
    # Fallback agar library install nahi hai to error batane ke liye
    print("WARNING: 'django-tabbed-admin' installed nahi hai. Tabs kaam nahi karenge.")
    TabbedModelAdmin = admin.ModelAdmin

from .models import (
    Company, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq,
    Followup, Meeting
)

# =====================================================
# 3. MIXINS (AUTO USER & AUDIT)
# =====================================================

class AutoUserAdminMixin:
    """
    Ye Mixin automatically created_by, updated_by aur uploaded_by 
    fields ko fill kar deta hai current logged-in user se.
    """
    def save_model(self, request, obj, form, change):
        # Create
        if hasattr(obj, "created_by") and not change and not obj.created_by:
            obj.created_by = request.user
        # Update
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        # Upload
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


# =====================================================
# 4. FORMSETS (VALIDATION LOGIC)
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
            raise ValidationError("❌ Ek company ke liye sirf 1 Active Followup allowed hai.")


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
            raise ValidationError("❌ Ek company ke liye sirf 1 Active Meeting allowed hai.")


# =====================================================
# 5. INLINE MODELS
# =====================================================

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0
    # exclude = ("created_by", "updated_by") # Optional: agar hidden rakhna ho

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0

class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    classes = ("tab-6-comments",) # CSS Class for styling if needed

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

class FollowupInline(admin.StackedInline):
    model = Followup
    formset = FollowupInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")
    classes = ("tab-3-followups",)

class MeetingInline(admin.StackedInline):
    model = Meeting
    formset = MeetingInlineFormSet
    extra = 1
    exclude = ("created_by", "updated_by", "create_at", "update_at")
    classes = ("tab-2-meetings",)


# =====================================================
# 6. COMPANY ADMIN (MAIN)
# =====================================================

@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, TabbedModelAdmin): # 🔥 CHANGED: Inherits TabbedModelAdmin
    
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'js/admin_dependent_dropdown.js',
        )

    list_display = (
        "id", "company_name", "category",
        "city", "locality", "sub_locality", "project",
        "contact_no", "status",
        "is_verified", "is_featured",
        "assigned_to", "created_by", "updated_by", "created_at", "updated_at"
    )

    list_filter = (
        "status", "category",
        "city", "locality", "sub_locality", "project",
        "is_verified", "is_featured",
        "assigned_to"
    )

    search_fields = ("company_name", "contact_no")
    
    readonly_fields = ("slug", "created_at", "updated_at", "logo_preview")

    # Fieldsets (Standard Admin View ke liye fallback)
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

    # Inlines list (Standard View ke liye)
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

    # 🔥 TABS CONFIGURATION (Tabbed Admin ke liye)
    tabs = [
        ("Company Info", (
            "company_name", "contact_no", "category", "city", 
            "locality", "sub_locality", "project", "address", 
            "status", "assigned_to", "whatsapp", "email", 
            "description", "logo", "logo_preview", 
            "is_active", "is_verified", "is_featured", "website", "google_map"
        )),
        ("4. Voice Recordings", (VoiceRecordingInline,)),
        ("5. Visits", (VisitInline,)),
        ("3. Followups", (FollowupInline,)),
        ("2. Meetings", (MeetingInline,)),
        ("6. Comments", (CommentInline,)),
        ("Images & Social", (ImagesInline, SocialLinkInline)), # Optional: Images aur Social ko ek tab me rakh sakte hain
        ("FAQ", (FaqInline,))
    ]

    list_per_page = 20


# =====================================================
# 7. OTHER ADMINS
# =====================================================

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        "id", "company_name", "company_city", "company_locality",
        "company_contact", "company_category", "status",
        "followup_date", "assigned_to", "created_by", "update_at"
    )
    list_filter = ("status", "assigned_to", "company__city", "company__category")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def company_name(self, obj): return obj.company.company_name
    company_name.short_description = "Company Name"
    company_name.admin_order_field = "company__company_name"

    def company_city(self, obj): return obj.company.city
    company_city.short_description = "City"
    company_city.admin_order_field = "company__city"

    def company_locality(self, obj): return obj.company.locality
    company_locality.short_description = "Locality"
    company_locality.admin_order_field = "company__locality"

    def company_contact(self, obj): return obj.company.contact_no
    company_contact.short_description = "Contact No"

    def company_category(self, obj): return obj.company.category
    company_category.short_description = "Category"


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        "id", "company_name", "company_city", "company_locality",
        "company_contact", "company_category", "status",
        "meeting_date", "assigned_to", "created_by", "update_at"
    )
    list_filter = ("status", "assigned_to", "company__city", "company__locality", "company__category")
    search_fields = ("company__company_name", "company__contact_no")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

    def company_name(self, obj): return obj.company.company_name
    company_name.short_description = "Company Name"
    company_name.admin_order_field = "company__company_name"

    def company_city(self, obj): return obj.company.city
    company_city.short_description = "City"
    company_city.admin_order_field = "company__city"

    def company_locality(self, obj): return obj.company.locality
    company_locality.short_description = "Locality"
    company_locality.admin_order_field = "company__locality"

    def company_contact(self, obj): return obj.company.contact_no
    company_contact.short_description = "Contact No"

    def company_category(self, obj): return obj.company.category
    company_category.short_description = "Category"


# 🔥 FIX: In sabko bhi AutoUserAdminMixin diya taaki 'created_by' save ho sake
@admin.register(Approx)
class ApproxAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

@admin.register(SocialLink)
class SocialLinkAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "social_site", "link")
    readonly_fields = ( "create_at", "update_at")

@admin.register(Error)
class ErrorAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")
    readonly_fields = ("created_by", "updated_by", "create_at", "update_at")

@admin.register(Images)
class ImagesAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "title", "image")

@admin.register(Faq)
class FaqAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    readonly_fields = ("create_at", "update_at")