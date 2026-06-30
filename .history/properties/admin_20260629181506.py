from django.contrib import admin
from django.utils.html import mark_safe
from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from django.utils.html import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Developer
from django.utils.html import format_html

from .models import (
    Project, BookingOffer, WelcomeTo, WebSlider, Overview, AboutUs,
    USP, Configuration, Connectivity, Amenities, Gallery, Header,
    RERA_Info, WhyInvest, BankOffer,Enquiry,ProjectFAQ,Architects,Engineer,ProjectContactPerson,Comment,VoiceRecording,Visit,Meeting,Followup
)

class BaseCRMAdmin(admin.ModelAdmin):

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def save_model(self, request, obj, form, change):
        ...


class AutoUserAdminMixin:

    def save_model(self, request, obj, form, change):

        if hasattr(obj, "created_by") and not obj.created_by:
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
            obj.uploaded_by = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):

        parent = form.instance

        instances = formset.save(commit=False)

        # Delete
        for obj in getattr(formset, "deleted_objects", []):
            obj.delete()

        # Save
        for obj in instances:

            if hasattr(obj, "created_by") and not obj.created_by:
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            if hasattr(obj, "uploaded_by") and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()

        formset.save_m2m()

        from .models import (
            Developer,
            Architects,
            Engineer,
            Project,
            Meeting,
            Followup,
        )

        model_map = {
            Developer: "developer",
            Architects: "architect",
            Engineer: "engineer",
            Project: "project",
        }

        field_name = None

        for model, field in model_map.items():
            if isinstance(parent, model):
                field_name = field
                break

        if not field_name:
            return

        meeting = Meeting.objects.filter(
            **{field_name: parent}
        ).exists()

        followup = Followup.objects.filter(
            **{field_name: parent}
        ).exists()

        if meeting and followup:
            status = "Meeting_FollowUp"

        elif meeting:
            status = "Meeting"

        elif followup:
            status = "FollowUp"

        else:
            status = "New"

        parent.__class__.objects.filter(
            pk=parent.pk
        ).update(
            calling_status=status
        )
# ============================================
# COMMENT INLINE
# ============================================

class CommentDeveloperInline(admin.StackedInline):
    model = Comment
    fk_name = "developer"
    extra = 0

    fields = (
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class CommentArchitectInline(admin.StackedInline):
    model = Comment
    fk_name = "architect"
    extra = 0

    fields = (
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class CommentEngineerInline(admin.StackedInline):
    model = Comment
    fk_name = "engineer"
    extra = 0

    fields = (
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class CommentProjectInline(admin.StackedInline):
    model = Comment
    fk_name = "project"
    extra = 0

    fields = (
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

# ============================================
# VOICE RECORDING INLINE
# ============================================

class VoiceDeveloperInline(admin.StackedInline):
    model = VoiceRecording
    fk_name = "developer"
    extra = 0

    fields = (
        "file",
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VoiceArchitectInline(admin.StackedInline):
    model = VoiceRecording
    fk_name = "architect"
    extra = 0

    fields = (
        "file",
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VoiceEngineerInline(admin.StackedInline):
    model = VoiceRecording
    fk_name = "engineer"
    extra = 0

    fields = (
        "file",
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VoiceProjectInline(admin.StackedInline):
    model = VoiceRecording
    fk_name = "project"
    extra = 0

    fields = (
        "file",
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

# ============================================
# VISIT INLINE
# ============================================

class VisitDeveloperInline(admin.StackedInline):
    model = Visit
    fk_name = "developer"
    extra = 0

    fields = (
        "visit_for",
        "visit_type",
        "visit_status",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VisitArchitectInline(admin.StackedInline):
    model = Visit
    fk_name = "architect"
    extra = 0

    fields = (
        "visit_for",
        "visit_type",
        "visit_status",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VisitEngineerInline(admin.StackedInline):
    model = Visit
    fk_name = "engineer"
    extra = 0

    fields = (
        "visit_for",
        "visit_type",
        "visit_status",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class VisitProjectInline(admin.StackedInline):
    model = Visit
    fk_name = "project"
    extra = 0

    fields = (
        "visit_for",
        "visit_type",
        "visit_status",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )



# ============================================
# FOLLOWUP INLINE
# ============================================

class FollowupDeveloperInline(admin.StackedInline):
    model = Followup
    fk_name = "developer"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "followup_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class FollowupArchitectInline(admin.StackedInline):
    model = Followup
    fk_name = "architect"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "followup_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class FollowupEngineerInline(admin.StackedInline):
    model = Followup
    fk_name = "engineer"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "followup_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class FollowupProjectInline(admin.StackedInline):
    model = Followup
    fk_name = "project"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "followup_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

# ============================================
# MEETING INLINE
# ============================================

class MeetingDeveloperInline(admin.StackedInline):
    model = Meeting
    fk_name = "developer"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class MeetingArchitectInline(admin.StackedInline):
    model = Meeting
    fk_name = "architect"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class MeetingEngineerInline(admin.StackedInline):
    model = Meeting
    fk_name = "engineer"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )


class MeetingProjectInline(admin.StackedInline):
    model = Meeting
    fk_name = "project"
    extra = 0
    max_num = 1

    fields = (
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "create_at",
        "update_at",
    )



# ✅ Placeholder image for missing logos
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import Developer

NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"


@admin.register(Developer)
#class DeveloperAdmin(AutoUserAdminMixin, ImportExportModelAdmin):
class DeveloperAdmin(AutoUserAdminMixin, admin.ModelAdmin):


    change_list_template = "admin/properties/developer/change_list.html"
    
    
    inlines = [
        CommentDeveloperInline,
        VoiceDeveloperInline,
        VisitDeveloperInline,
        FollowupDeveloperInline,
        MeetingDeveloperInline,
    ]
    list_display = (
        'id',
        'calling_status',
        'title',
        'city',
        'locality',
        'postal_code',
        'address',
        'contact_person',
        'contact_no',
        'email',
        'web_site',
        'featured_builder',
        'created_date',
        'updated_date',
        'logo_preview',
    )

    list_filter = (
        'city',
        'locality',
        'postal_code',
        'featured_builder',
        'create_at',
    )

    search_fields = (
        'title',

        # Postal Code
        'postal_code__postal_code',
        'postal_code__postal_name',

        # Other Fields
        'address',
        'keywords',
        'contact_person',
        'contact_no',
        'email',
        'note',
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        'create_at',
        'update_at',
        'logo_preview',
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    'calling_status',

                    "city",
                    "locality",
                    "postal_code",
                    "address",
                    "contact_person",
                    "contact_no",
                    "email",
                    "web_site",
                    "featured_builder",
                )
            },
        ),
        (
            "SEO & Content",
            {
                "fields": (
                    "keywords",
                    "about_developer",
                    "logo",
                    "logo_preview",
                    "google_map",
                    "slug",
                    "create_at",
                    "update_at",
                    "note",
                )
            },
        ),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;">',
                obj.logo.url,
            )
        return format_html(
            '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;">',
            NO_IMAGE_URL,
        )

    logo_preview.short_description = "Logo"

    def created_date(self, obj):
        return obj.create_at.strftime("%d %b %Y")

    created_date.short_description = "Created"

    def updated_date(self, obj):
        return obj.update_at.strftime("%d %b %Y")

    updated_date.short_description = "Updated"


@admin.register(Architects)
class ArchitectsAdmin(AutoUserAdminMixin, ImportExportModelAdmin):
    
    inlines = [
        CommentArchitectInline,
        VoiceArchitectInline,
        VisitArchitectInline,
        FollowupArchitectInline,
        MeetingArchitectInline,
    ]
    
    list_display = (
        'id',
        'calling_status',
        'title',
        'city',
        'locality',
        'address',
        'postal_code',
        'contact_person', 'contact_no', 'email', 'web_site',
        'note',
        'featured_architect',
        'created_date',
        'updated_date',
        'logo_preview',
    )
    list_filter = ('city', 'locality','featured_architect', 'create_at', 'update_at')
    search_fields = ('title','postal_code_postal_code', 'keywords', 'contact_person','contact_no','note','address',)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('create_at', 'update_at', 'logo_preview')

    fieldsets = (
        ('Basic Information', {
            'fields':('title', 'calling_status',  'city', 'locality', 'address','postal_code','contact_person', 'contact_no', 'email', 'web_site','featured_architect',)
        }),
        
        ('SEO & Content', {
            'fields': ('keywords', 'about_architect','logo', 'logo_preview', 'google_map','slug','create_at', 'update_at')
        }),
       
    )

    def logo_preview(self, obj):
        if obj.logo and obj.logo.name:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;" />',
                obj.logo.url
            )

        return format_html(
            '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;" />',
            NO_IMAGE_URL
        )

    logo_preview.short_description = "Logo Preview"
        

    def created_date(self, obj):
        return obj.create_at.strftime('%d %b %Y')
    created_date.short_description = "Created"

    def updated_date(self, obj):
        return obj.update_at.strftime('%d %b %Y')
    updated_date.short_description = "Updated"

@admin.register(Engineer)
class EngineerAdmin(AutoUserAdminMixin, ImportExportModelAdmin):
    
    inlines = [
        CommentEngineerInline,
        VoiceEngineerInline,
        VisitEngineerInline,
        FollowupEngineerInline,
        MeetingEngineerInline,
    ]
    
    list_display = (
        'id',
        'calling_status',
        'title',
        'city',
        'locality',
        'address',
        'postal_code',
        'contact_person', 'contact_no', 'email', 'web_site',
        'note',
        'featured_engineer',
        'created_date',
        'updated_date',
        'logo_preview',
    )
    list_filter = ('city', 'locality','postal_code','featured_engineer', 'create_at', 'update_at')
    search_fields = ('title','postal_code_postal_code', 'keywords', 'contact_person','contact_no','note','address',)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('create_at', 'update_at', 'logo_preview')

    fieldsets = (
        ('Basic Information', {
            'fields':('title', 'calling_status', 'city', 'locality', 'address','postal_code','contact_person', 'contact_no', 'email', 'web_site','featured_engineer',)
        }),
        
        ('SEO & Content', {
            'fields': ('keywords', 'about_engineer','logo', 'logo_preview', 'google_map','slug','create_at', 'update_at')
        }),
       
    )

    def logo_preview(self, obj):
        if obj.logo and obj.logo.name:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;" />',
                obj.logo.url
            )

        return format_html(
            '<img src="{}" width="80" height="80" style="object-fit:contain;border:1px solid #ddd;border-radius:6px;" />',
            NO_IMAGE_URL
        )

    logo_preview.short_description = "Logo Preview"
        

    def created_date(self, obj):
        return obj.create_at.strftime('%d %b %Y')
    created_date.short_description = "Created"

    def updated_date(self, obj):
        return obj.update_at.strftime('%d %b %Y')
    updated_date.short_description = "Updated"

class ProjectContactPersonInline(admin.StackedInline):
    model = ProjectContactPerson
    extra = 1

    fields = (
        "name",
        "designation",
        "mobile",
        "whatsapp",
        "email",
        "is_primary",
    )

class BookingOfferInline(admin.TabularInline):
    model = BookingOffer
    extra = 1

class WelcomeToInline(admin.StackedInline):
    model = WelcomeTo
    extra = 1

class ProjectFAQInline(admin.TabularInline):
    model = ProjectFAQ
    extra = 1
    fields = ("order", "question", "answer")

class WebSliderInline(admin.TabularInline):
    model = WebSlider
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
        else:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">')
    image_preview.short_description = "Preview"

class OverviewInline(admin.StackedInline):
    model = Overview
    extra = 1

class AboutUsInline(admin.StackedInline):
    model = AboutUs
    extra = 1


class USPInline(admin.TabularInline):
    model = USP
    extra = 1


class ConfigurationInline(admin.TabularInline):
    model = Configuration
    extra = 1


class ConnectivityInline(admin.TabularInline):
    model = Connectivity
    extra = 1


class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
        else:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">')
    image_preview.short_description = "Preview"


class HeaderInline(admin.StackedInline):
    model = Header
    extra = 1


class RERAInfoInline(admin.StackedInline):
    model = RERA_Info
    extra = 1


class WhyInvestInline(admin.StackedInline):
    model = WhyInvest
    extra = 1


class BankOfferInline(admin.TabularInline):
    model = BankOffer
    extra = 1


@admin.register(Project)
class ProjectAdmin(AutoUserAdminMixin, MPTTModelAdmin):
    list_display = (
        'project_name', 'city', 'locality','postal_code', 'developer','architects','engineer',
        'construction_status', 'possession_month', 'possession_year',
        'featured_property', 'active', 'image_preview', 'youtube_preview'
    )

    list_filter = (
        'city', 'developer','postal_code', 'architects','engineer','propert_type',
        'construction_status', 'featured_property', 'active'
    )

    search_fields = (
        'project_name',
        'city__name',
        'locality__name',
        'developer__title',
        'architects_title',
        'engineer_title',
        'postal_code_postal_code',
    )

    prepopulated_fields = {"slug": ("project_name",)}

    readonly_fields = (
        'create_at',
        'update_at',
        'image_preview',
        'youtube_preview'
    )

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'project_name', 'slug', 'parent', 'developer',
                'city', 'locality','postal_code', 'propert_type',
                'image',
                'construction_status',
                'image_preview',
                'youtube_embed_id', 'youtube_preview',
                'create_at', 'update_at',
                'google_map_iframe',      
            )
        }),
        ('More Info', {
            'fields': (
                
                'bhk_type',
                'floor', 'land_parcel', 'luxurious', 'priceing',
                'possession_month', 'possession_year',
                'Occupancy_Certificate',
                'Commencement_Certificate',
                'featured_property',
                'active',
                'architects',
                'engineer',
                
            )
        }),
    )

    # 🔥 UPDATED INLINES (FAQ ADDED)
    inlines = [
        BookingOfferInline,
        WelcomeToInline,
        WebSliderInline,
        OverviewInline,
        AboutUsInline,
        USPInline,
        ConfigurationInline,
        ConnectivityInline,
        AmenitiesInline,
        GalleryInline,
        HeaderInline,
        RERAInfoInline,
        WhyInvestInline,
        BankOfferInline,
        ProjectFAQInline,
        ProjectContactPersonInline, 
        CommentProjectInline,
        VoiceProjectInline,
        VisitProjectInline,
        FollowupProjectInline,
        MeetingProjectInline,
    ]

    class MPTTMeta:
        order_insertion_by = ['project_name']

    # ---------- PREVIEWS ----------
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="50" '
                f'style="object-fit:cover;border-radius:6px;">'
            )
        return mark_safe(
            '<img src="https://via.placeholder.com/80x50.png?text=No+Image">'
        )
    image_preview.short_description = "Preview"

    def youtube_preview(self, obj):
        if obj.youtube_embed_id:
            vid = obj.youtube_embed_id.strip()
            thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            url = f"https://www.youtube.com/watch?v={vid}"
            return mark_safe(
                f'<a href="{url}" target="_blank">'
                f'<img src="{thumb}" width="120" height="80" '
                f'style="object-fit:cover;border-radius:6px;">'
                f'</a>'
            )
        return "No Video"
    youtube_preview.short_description = "YouTube Preview"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'phone', 'email', 'project', 'message', 'contacted_on']
    list_filter = ('project', 'contacted_on')
    search_fields = ('name', 'email', 'phone', 'message', 'project__project_name')
    ordering = ('-contacted_on',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "comment",
        "created_by",
        "create_at",
    )

    list_filter = ("type",)

    search_fields = (
        "comment",
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
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


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "uploaded_by",
        "create_at",
    )

    list_filter = ("type",)

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
    )

    readonly_fields = (
        "uploaded_by",
        "updated_by",
        "create_at",
        "update_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):



    list_display = (
        "id",
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "visit_type",
        "visit_status",
        "created_by",
        "create_at",
    )

    list_filter = (
        "type",
        "visit_status",
        "visit_type",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
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


@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "status",
        "followup_date",
        "assigned_to",
        "created_by",
        "create_at",
    )

    list_filter = (
        "type",
        "status",
        "followup_date",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
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

    list_display = (
        "id",
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "status",
        "meeting_date",
        "assigned_to",
        "created_by",
        "create_at",
    )

    list_filter = (
        "type",
        "status",
        "meeting_date",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
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



