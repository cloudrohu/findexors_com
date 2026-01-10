from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, BooleanWidget

from .models import (
    Company,
    Category,
    City,
    Locality,
    Sub_Locality,
    Project,
)

# ============================================================
# COMPANY RESOURCE (IMPORT / EXPORT)
# ============================================================

class CompanyResource(resources.ModelResource):

    # -------- FK FIELDS (CSV NAME → MODEL) --------
    category = Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, "title"),
    )

    city = Field(
        column_name="city",
        attribute="city",
        widget=ForeignKeyWidget(City, "title"),
    )

    locality = Field(
        column_name="locality",
        attribute="locality",
        widget=ForeignKeyWidget(Locality, "title"),
    )

    sub_locality = Field(
        column_name="sub_locality",
        attribute="sub_locality",
        widget=ForeignKeyWidget(Sub_Locality, "title"),
    )

    project = Field(
        column_name="project",
        attribute="project",
        widget=ForeignKeyWidget(Project, "title"),
    )

    is_verified = Field(
        column_name="verified",
        attribute="is_verified",
        widget=BooleanWidget(),
    )

    # ========================================================
    class Meta:
        model = Company

        import_id_fields = ("contact_no",)   # 🔥 Duplicate avoid
        skip_unchanged = True
        report_skipped = True

        fields = (
            "company_name",
            "contact_no",
            "email",
            "website",
            "address",
            "description",
            "status",
            "category",
            "city",
            "locality",
            "sub_locality",
            "project",
            "is_verified",
        )

        export_order = fields

    # ========================================================
    # CLEANING LOGIC
    # ========================================================
    def before_import_row(self, row, **kwargs):
        # Phone clean
        if row.get("contact_no"):
            row["contact_no"] = str(row["contact_no"]).replace(" ", "")

        # Default status
        if not row.get("status"):
            row["status"] = "New"

    # ========================================================
    # AUTO CREATE FK DATA (City / Locality etc.)
    # ========================================================
    def before_save_instance(self, instance, row, **kwargs):

        if row.get("category"):
            instance.category, _ = Category.objects.get_or_create(
                title=row["category"]
            )

        if row.get("city"):
            instance.city, _ = City.objects.get_or_create(
                title=row["city"]
            )

        if row.get("locality"):
            instance.locality, _ = Locality.objects.get_or_create(
                title=row["locality"],
                city=instance.city
            )

        if row.get("sub_locality"):
            instance.sub_locality, _ = Sub_Locality.objects.get_or_create(
                title=row["sub_locality"],
                locality=instance.locality
            )

        if row.get("project"):
            instance.project, _ = Project.objects.get_or_create(
                title=row["project"]
            )
