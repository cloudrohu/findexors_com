from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import GoogleCompany
from .resources_clean import GoogleCompanyResource

@admin.register(GoogleCompany)
class GoogleCompanyAdmin(ImportExportModelAdmin):
    resource_class = GoogleCompanyResource
    list_display = ("id", "name", "phone", "city_text", "state", "rating", "reviews")
    search_fields = ("name", "phone", "place_id")
    list_filter = ("state", "country")
