from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.html import mark_safe
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from .models import City, Locality, PropertyType, PossessionIn, ProjectAmenities, Bank


# 🟡 Placeholder image URL (fallback)
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

from .models import (
    City, Locality,
    Find_Form, Call_Status, SocialSite,
    Googlemap_Status, Response_Status, RequirementType,Category,Sub_Locality
)

@admin.register(Sub_Locality)
class SubLocalityAdmin(admin.ModelAdmin):
    list_display = ('title', 'locality', 'create_at', 'update_at')
    list_filter = ('locality', 'create_at')
    search_fields = ('title', 'locality__title')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-create_at',)
    date_hierarchy = 'create_at'

    # Optional: to auto-fill locality for b

# ------------------------------
# Resources for Import/Export
# ------------------------------


# Resource for import-export
class LocalityResource(resources.ModelResource):
    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=ForeignKeyWidget(Locality, "title")  # parent ko title ke base par match karega
    )

    class Meta:
        model = Locality
        fields = ("id", "title", "parent", "slug")
        import_id_fields = ("id",)


# Admin
@admin.register(Locality)
class LocalityAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    resource_class = LocalityResource
    mptt_indent_field = "title"
    list_display = ("id",'city', "tree_actions", "indented_title", "slug")
    list_display_links = ("indented_title",)
    list_per_page = 30
    prepopulated_fields = {"slug": ("title",)}


class FindFormResource(resources.ModelResource):
    class Meta:
        model = Find_Form
        fields = "__all__"

class CallStatusResource(resources.ModelResource):
    class Meta:
        model = Call_Status
        fields = "__all__"

class SocialSiteResource(resources.ModelResource):
    class Meta:
        model = SocialSite
        fields = "__all__"

class GooglemapStatusResource(resources.ModelResource):
    class Meta:
        model = Googlemap_Status
        fields = "__all__"

class ResponseStatusResource(resources.ModelResource):
    class Meta:
        model = Response_Status
        fields = "__all__"

class RequirementTypeResource(resources.ModelResource):
    class Meta:
        model = RequirementType
        fields = "__all__"


# ------------------------------
# Admin Classes
# ------------------------------
# Resource
class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ("id", "title")   # sirf id aur title
        import_id_fields = ("id",) # id optional hai import ke time


# Admin
@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ("id", "title")
    search_fields = ("title",)



@admin.register(Find_Form)
class FindFormAdmin(ImportExportModelAdmin):
    resource_class = FindFormResource
    list_display = ("id", "__str__")

@admin.register(Call_Status)
class CallStatusAdmin(ImportExportModelAdmin):
    resource_class = CallStatusResource
    list_display = ("id", "__str__")

@admin.register(SocialSite)
class SocialSiteAdmin(ImportExportModelAdmin):
    resource_class = SocialSiteResource
    list_display = ("id", "__str__")

@admin.register(Googlemap_Status)
class GooglemapStatusAdmin(ImportExportModelAdmin):
    resource_class = GooglemapStatusResource
    list_display = ("id", "__str__")

@admin.register(Response_Status)
class ResponseStatusAdmin(ImportExportModelAdmin):
    resource_class = ResponseStatusResource
    list_display = ("id", "__str__")

@admin.register(RequirementType)
class RequirementTypeAdmin(ImportExportModelAdmin):
    resource_class = RequirementTypeResource
    list_display = ("id", "__str__")

# ======================================================
# CATEGORY ADMIN
# ======================================================


from django.utils.html import format_html


class CategoryAdmin(DraggableMPTTAdmin):

    mptt_indent_field = "title"

    list_display = (
        "tree_actions",
        "indented_title",
        "safe_icon_tag",
        "is_featured",
        "slug",
        "create_at",
    )

    list_display_links = ("indented_title",)

    search_fields = ("title",)

    prepopulated_fields = {"slug": ("title",)}

    list_filter = ("is_featured", "create_at")

    readonly_fields = ("safe_icon_tag",)

    list_per_page = 30

    ordering = ("title",)

    # 🔐 FULLY SAFE ICON RENDER
    def safe_icon_tag(self, obj):
        """
        Icon field ho ya na ho,
        DB me column missing ho tab bhi
        admin crash nahi karega
        """
        try:
            if hasattr(obj, "icon") and obj.icon:
                return format_html(
                    '<img src="{}" style="height:30px;width:auto;border-radius:4px;" />',
                    obj.icon.url
                )
        except Exception:
            pass
        return "—"

    safe_icon_tag.short_description = "Icon"



admin.site.register(Category, CategoryAdmin)


@admin.register(PropertyType)
class PropertyTypeAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'is_top_level', 'is_selectable')
    list_filter = ('is_top_level', 'is_selectable')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 20

    fieldsets = (
        ('Property Type Info', {
            'fields': ('name', 'slug', 'parent', 'is_top_level', 'is_selectable')
        }),
    )

# =======================================================
# 📅 PossessionIn Admin
# =======================================================
@admin.register(PossessionIn)
class PossessionInAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('year',)
    search_fields = ('year',)

@admin.register(ProjectAmenities)
class ProjectAmenitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview')

    def preview(self, obj):
        """Display safe image preview in Django admin."""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return mark_safe(
                    f'<img src="{obj.image.url}" width="80" height="80" '
                    f'style="object-fit:cover;border-radius:8px;" />'
                )
        except Exception:
            pass
        return mark_safe(
            '<img src="https://via.placeholder.com/80x80.png?text=No+Image" '
            'style="object-fit:cover;border-radius:8px;" />'
        )

    preview.short_description = "Preview"



# =======================================================
# 🏦 Bank Admin
# =======================================================
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('title', 'safe_image_preview')
    search_fields = ('title',)
    readonly_fields = ('safe_image_preview',)

    def safe_image_preview(self, obj):
        """Safe logo preview (never crashes even if image missing)."""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                url = obj.image.url
            else:
                url = NO_IMAGE_URL
        except Exception:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="60" height="60" '
                         f'style="object-fit:contain;border-radius:6px;" />')

    safe_image_preview.short_description = "Logo"


