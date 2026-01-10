from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Company, City, Category
from django.contrib.auth.models import User


class CompanyResource(resources.ModelResource):

    city = fields.Field(
        column_name="city",
        attribute="city",
        widget=ForeignKeyWidget(City, "name")
    )

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, "name")
    )

    created_by = fields.Field(
        column_name="created_by",
        attribute="created_by",
        widget=ForeignKeyWidget(User, "username")
    )

    class Meta:
        model = Company

        # 🔥 Duplicate control
        import_id_fields = ("contact_no",)

        skip_unchanged = True
        report_skipped = True

        fields = (
            "company_name",
            "contact_no",
            "email",
            "website",
            "address",
            "description",
            "city",
            "category",
            "status",
            "is_verified",
            "is_active",
            "created_by",
        )
