from import_export import resources, fields
from import_export.widgets import DateTimeWidget

from .models import GoogleCompany


class GoogleCompanyResource(resources.ModelResource):
    class Meta:
        model = GoogleCompany
        import_id_fields = ("place_id",)  # unique key
        skip_unchanged = True
        report_skipped = True
        fields = (
            "id",
            "name",
            "name_for_emails",
            "category_text",
            "type",
            "phone",
            "website",
            "address",
            "street",
            "city_text",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "rating",
            "reviews",
            "business_status",
            "working_hours",
            "description",
            "about",
            "logo",
            "place_id",
            "google_id",
            "cid",
            "created_at",
            "updated_at",
        )
