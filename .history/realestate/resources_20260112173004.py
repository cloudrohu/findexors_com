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
        ✅ Fix all CSV mapping issues:
        - city_name -> city_text
        - category_name -> category_text (if exists)
        - phone clean
        - auto FK mapping
        """

        # --------------------------------------------------
        # ✅ 1) Normalize keys (CSV headers)
        # --------------------------------------------------
        # city_name -> city_text
        if row.get("city_name") and not row.get("city_text"):
            row["city_text"] = row.get("city_name")

        # category_name -> category_text
        if row.get("category_name") and not row.get("category_text"):
            row["category_text"] = row.get("category_name")

        # locality_name -> street (optional)
        if row.get("locality_name") and not row.get("street"):
            row["street"] = row.get("locality_name")

        # --------------------------------------------------
        # ✅ 2) Phone Clean
        # --------------------------------------------------
        phone = (row.get("phone") or "").strip()
        if phone:
            phone = phone.replace(" ", "")
        row["phone"] = phone

        # --------------------------------------------------
        # ✅ 3) CITY FK mapping
        # --------------------------------------------------
        city_name = (row.get("city_text") or "").strip()

        if city_name:
            city_obj, _ = City.objects.get_or_create(city_name=city_name)
            row["city"] = city_obj.id
        else:
            fallback_city, _ = City.objects.get_or_create(city_name="Unknown")
            row["city"] = fallback_city.id
            row["city_text"] = "Unknown"

        # --------------------------------------------------
        # ✅ 4) CATEGORY FK mapping
        # --------------------------------------------------
        cat_name = (row.get("category_text") or "").strip()
        if cat_name:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_name)
            row["category"] = cat_obj.id

        # --------------------------------------------------
        # ✅ 5) LOCALITY FK mapping
        # --------------------------------------------------
        loc_name = (row.get("street") or row.get("address") or "").strip()
        if loc_name and len(loc_name) > 2:
            locality_obj, _ = Locality.objects.get_or_create(
                locality_name=loc_name[:200],
                city_id=row.get("city")
            )
            row["locality"] = locality_obj.id
