from import_export import resources
from .models import GoogleCompany
from utility.models import City, Category, Locality


class GoogleCompanyResource(resources.ModelResource):

    class Meta:
        model = GoogleCompany
        import_id_fields = ("place_id",)
        skip_unchanged = True
        report_skipped = True

        fields = (
            "id",
            "name",
            "name_for_emails",
            "category",
            "city",
            "locality",

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

    def before_import_row(self, row, **kwargs):
        """
        ✅ Outscraper import safe mapper:
        - city_text => City FK
        - category_text => Category FK
        - street/address => Locality FK
        """

        # ✅ Phone clean
        phone = (row.get("phone") or "").strip()
        if phone:
            phone = phone.replace(" ", "")
        row["phone"] = phone

        # ✅ CITY mapping
        city_name = (row.get("city_text") or "").strip()
        if city_name:
            city_obj, _ = City.objects.get_or_create(city_name=city_name)
            row["city"] = city_obj.id
        else:
            # fallback city to avoid crash
            fallback_city, _ = City.objects.get_or_create(city_name="Unknown")
            row["city"] = fallback_city.id
            row["city_text"] = "Unknown"

        # ✅ CATEGORY mapping
        cat_name = (row.get("category_text") or "").strip()
        if cat_name:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_name)
            row["category"] = cat_obj.id

        # ✅ LOCALITY mapping (street preferred)
        loc_name = (row.get("street") or row.get("address") or "").strip()
        if loc_name and len(loc_name) > 2:
            locality_obj, _ = Locality.objects.get_or_create(
                locality_name=loc_name[:200],  # safety
                city_id=row.get("city")
            )
            row["locality"] = locality_obj.id
