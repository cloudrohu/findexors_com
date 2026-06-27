from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django.utils.html import format_html, mark_safe

from .models import (
    City, Locality, Sub_Locality,
    PropertyType, PossessionIn,
    ProjectAmenities, Bank,
    Find_Form, Call_Status,
    SocialSite, Googlemap_Status,
    Response_Status, RequirementType,
    Category,Postal_Code
)

# ======================================================
# 🔹 CONSTANT
# ======================================================
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

@admin.register(Postal_Code)
class Postal_CodeAdmin(admin.ModelAdmin):

    list_display = ("postal_name","postal_code")
    ordering = ("postal_name","postal_code")
    search_fields = ("postal_name","postal_code")
    list_per_page = 30



# ======================================================
# 🔹 LOCALITY IMPORT EXPORT
# ======================================================
class LocalityResource(resources.ModelResource):
    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=ForeignKeyWidget(Locality, "title")
    )

    class Meta:
        model = Locality
        fields = ("id", "title", "city", "parent", "slug")
        import_id_fields = ("id",)


# ======================================================
# 🔹 CITY ADMIN
# ======================================================
@admin.register(City)
class CityAdmin(MPTTModelAdmin):

    list_display = (
        "id",
        "name",
        "level_type",
        "parent",
        "slug",
    )

    list_filter = (
        "level_type",
        "parent",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {"slug": ("name",)}

    mptt_level_indent = 20

    ordering = ("name",)

    list_per_page = 30


# ======================================================
# 🔹 LOCALITY ADMIN (IMPORTANT FOR AUTOCOMPLETE)
# ======================================================
@admin.register(Locality)
class LocalityAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):

    resource_class = LocalityResource
    mptt_indent_field = "title"

    list_display = (
        "id",
        "city",
        "tree_actions",
        "indented_title",
        "slug",
    )

    list_display_links = ("indented_title",)

    list_filter = (
        "city",
    )

    search_fields = (
        "title",
        "slug",
        "city__name",
    )

    prepopulated_fields = {"slug": ("title",)}

    ordering = ("title",)

    list_per_page = 30


# ======================================================
# 🔹 SUB LOCALITY ADMIN
# ======================================================
@admin.register(Sub_Locality)
class SubLocalityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "locality",
        "slug",
        "create_at",
        "update_at",
    )

    list_filter = (
        "locality",
        "create_at",
    )

    search_fields = (
        "title",
        "slug",
        "locality__title",
    )

    prepopulated_fields = {"slug": ("title",)}

    ordering = ("-create_at",)

    date_hierarchy = "create_at"

    list_per_page = 30


# ======================================================
# 🔹 CATEGORY ADMIN (MPTT SAFE)
# ======================================================
@admin.register(Category)
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

    list_filter = (
        "is_featured",
        "create_at",
    )

    search_fields = (
        "title",
        "slug",
    )

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("safe_icon_tag",)

    ordering = ("title",)

    list_per_page = 30

    def safe_icon_tag(self, obj):
        try:
            if hasattr(obj, "icon") and obj.icon:
                return format_html(
                    '<img src="{}" style="height:30px;border-radius:6px;" />',
                    obj.icon.url
                )
        except Exception:
            pass
        return "—"

    safe_icon_tag.short_description = "Icon"


# ======================================================
# 🔹 PROPERTY TYPE ADMIN
# ======================================================
@admin.register(PropertyType)
class PropertyTypeAdmin(MPTTModelAdmin):

    list_display = (
        "id",
        "name",
        "parent",
        "is_top_level",
        "is_selectable",
        "slug",
    )

    list_filter = (
        "is_top_level",
        "is_selectable",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {"slug": ("name",)}

    mptt_level_indent = 20

    ordering = ("name",)

    list_per_page = 30


# ======================================================
# 🔹 POSSESSION ADMIN
# ======================================================
@admin.register(PossessionIn)
class PossessionInAdmin(admin.ModelAdmin):

    list_display = ("id", "year")
    ordering = ("year",)
    search_fields = ("year",)
    list_per_page = 30


# ======================================================
# 🔹 PROJECT AMENITIES ADMIN
# ======================================================
@admin.register(ProjectAmenities)
class ProjectAmenitiesAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "preview",
    )

    search_fields = ("title",)

    list_per_page = 30

    def preview(self, obj):
        try:
            if obj.image and hasattr(obj.image, "url"):
                return mark_safe(
                    f'<img src="{obj.image.url}" width="70" '
                    f'style="border-radius:8px;object-fit:cover;" />'
                )
        except Exception:
            pass

        return mark_safe(
            f'<img src="{NO_IMAGE_URL}" width="70" '
            f'style="border-radius:8px;" />'
        )

    preview.short_description = "Image Preview"


@admin.register(RequirementType)
class RequirementTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

# ======================================================
# 🔹 BANK ADMIN
# ======================================================
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "safe_image_preview",
    )

    search_fields = ("title",)

    readonly_fields = ("safe_image_preview",)

    list_per_page = 30

    def safe_image_preview(self, obj):
        try:
            if obj.image and hasattr(obj.image, "url"):
                url = obj.image.url
            else:
                url = NO_IMAGE_URL
        except Exception:
            url = NO_IMAGE_URL

        return mark_safe(
            f'<img src="{url}" width="60" '
            f'style="object-fit:contain;border-radius:6px;" />'
        )

    safe_image_preview.short_description = "Logo"

