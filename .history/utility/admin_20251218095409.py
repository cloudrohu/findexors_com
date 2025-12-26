import admin_thumbnails
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


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
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ("tree_actions", "indented_title", "slug", "create_at")
    list_display_links = ("indented_title",)
    search_fields = ("title", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 30



admin.site.register(Category, CategoryAdmin)
