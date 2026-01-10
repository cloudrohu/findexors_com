from import_export import resources, fields
from import_export.widgets import DateTimeWidget
from .models import GoogleCompany


class GoogleCompanyResource(resources.ModelResource):
    # ✅ Custom mapping (CSV column → model field)
    name = fields.Field(attribute="name", column_name="name")
    name_for_emails = fields.Field(attribute="name_for_emails", column_name="name_for_emails")

    category_text = fields.Field(attribute="category_text", column_name="category")
    type = fields.Field(attribute="type", column_name="type")

    phone = fields.Field(attribute="phone", column_name="phone")
    website = fields.Field(attribute="website", column_name="website")

    address = fields.Field(attribute="address", column_name="address")
    street = fields.Field(attribute="street", column_name="street")

    city_text = fields.Field(attribute="city_text", column_name="city")
    state = fields.Field(attribute="state", column_name="state")
    postal_code = fields.Field(attribute="postal_code", column_name="postal_code")
    country = fields.Field(attribute="country", column_name="country")

    latitude = fields.Field(attribute="latitude", column_name="latitude")
    longitude = fields.Field(attribute="longitude", column_name="longitude")

    rating = fields.Field(attribute="rating", column_name="rating")
    reviews = fields.Field(attribute="reviews", column_name="reviews")

    place_id = fields.Field(attribute="place_id", column_name="place_id")
    google_id = fields.Field(attribute="google_id", column_name="google_id")
    cid = fields.Field(attribute="cid", column_name="cid")

    business_status = fields.Field(attribute="business_status", column_name="business_status")
    working_hours = fields.Field(attribute="working_hours", column_name="working_hours")

    about = fields.Field(attribute="about", column_name="about")
    description = fields.Field(attribute="description", column_name="description")

    logo = fields.Field(attribute="logo", column_name="logo")

    class Meta:
        model = GoogleCompany
        skip_unchanged = True
        report_skipped = True

        # ✅ Unique key for update existing rows
        import_id_fields = ("place_id",)

        # ✅ Field list (safe)
        fields = (
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
            "place_id",
            "google_id",
            "cid",
            "business_status",
            "working_hours",
            "about",
            "description",
            "logo",
        )
