from import_export import resources, fields
from .models import GoogleCompany


def clean_text(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def clean_phone(value):
    value = clean_text(value)
    if not value:
        return None
    value = (
        value.replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
    return value


def clean_decimal(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return float(value)
    except:
        return None


def clean_int(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return int(float(value))
    except:
        return None


class GoogleCompanyResource(resources.ModelResource):

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

        # ✅ update if place_id same
        import_id_fields = ("place_id",)

        skip_unchanged = True
        report_skipped = True

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

    # ✅ working in your version (No SkipRow dependency)
    def before_import_row(self, row, **kwargs):

        place_id = clean_text(row.get("place_id"))
        if not place_id:
            # ✅ row skip quietly
            row["__skip__"] = True
            return

        row["place_id"] = place_id
        row["name"] = clean_text(row.get("name"))
        row["name_for_emails"] = clean_text(row.get("name_for_emails"))

        row["category"] = clean_text(row.get("category"))
        row["type"] = clean_text(row.get("type"))

        row["phone"] = clean_phone(row.get("phone"))
        row["website"] = clean_text(row.get("website"))

        row["address"] = clean_text(row.get("address"))
        row["street"] = clean_text(row.get("street"))

        row["city"] = clean_text(row.get("city"))
        row["state"] = clean_text(row.get("state"))
        row["postal_code"] = clean_text(row.get("postal_code"))
        row["country"] = clean_text(row.get("country"))

        row["latitude"] = clean_decimal(row.get("latitude"))
        row["longitude"] = clean_decimal(row.get("longitude"))

        row["rating"] = clean_decimal(row.get("rating"))
        row["reviews"] = clean_int(row.get("reviews"))

        row["google_id"] = clean_text(row.get("google_id"))
        row["cid"] = clean_text(row.get("cid"))
        row["business_status"] = clean_text(row.get("business_status"))
        row["working_hours"] = clean_text(row.get("working_hours"))

        row["about"] = clean_text(row.get("about"))
        row["description"] = clean_text(row.get("description"))
        row["logo"] = clean_text(row.get("logo"))

    # ✅ skip row safely (this is best way without SkipRow)
    def import_row(self, row, instance_loader, **kwargs):
        if row.get("__skip__"):
            return None
        return super().import_row(row, instance_loader, **kwargs)
