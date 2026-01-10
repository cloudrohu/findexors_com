from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import (   # 🔥 YAHI MAIN FIX
    Company,
    Category,
    City,
    Locality,
    Sub_Locality,
    Project
)

class AutoCreateFKWidget(ForeignKeyWidget):
    """
    Agar CSV me value mile aur DB me na ho,
    to automatically create kar de.
    """

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None

        obj, created = self.model.objects.get_or_create(
            **{self.field: value.strip()}
        )
        return obj


class CompanyResource(resources.ModelResource):

    category = Field(
        column_name="category",
        attribute="category",
        widget=AutoCreateFKWidget(Category, "title")
    )

    city = Field(
        column_name="city",
        attribute="city",
        widget=AutoCreateFKWidget(City, "title")
    )

    locality = Field(
        column_name="locality",
        attribute="locality",
        widget=AutoCreateFKWidget(Locality, "title")
    )

    class Meta:
        model = Company
        import_id_fields = ("contact_no",)
        skip_unchanged = True
        report_skipped = True

        fields = (
            "company_name",
            "contact_no",
            "website",
            "address",
            "description",
            "category",
            "city",
            "locality",
            "status",
            "is_active",
        )

    # 🔥 OUTSCRAPER COLUMN MAPPING
    def before_import_row(self, row, **kwargs):
        row["company_name"] = row.get("name")
        row["contact_no"] = row.get("phone")
        row["description"] = row.get("about") or row.get("description")
        row["status"] = "New"
        row["is_active"] = True
