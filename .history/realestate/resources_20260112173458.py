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
            "id", "name", "name_for_emails",
            "category", "city", "locality",
            "category_text", "type", "phone", "website",
            "address", "street",
            "city_text", "state", "postal_code", "country",
            "latitude", "longitude",
            "rating", "reviews",
            "business_status", "working_hours",
            "description", "about", "logo",
            "place_id", "google_id", "cid",
            "created_at", "updated_at",
        )

    def get_city_obj(self, city_name):
        """
        ✅ City model me jo bhi field ho (name/title/city/city_name),
        uske basis pe get_or_create karega.
        """
        possible_fields = ["city_name", "name", "title", "city"]

        for f in possible_fields:
            if f in [field.name for field in City._meta.fields]:
                obj, _ = City.objects.get_or_create(**{f: city_name})
                return obj

        # agar match na mile
        return None

    def before_import_row(self, row, **kwargs):

        # ✅ CSV normalize
        if row.get("city_name") and not row.get("city_text"):
            row["city_text"] = row.get("city_name")

        if row.get("category_name") and not row.get("category_text"):
            row["category_text"] = row.get("category_name")

        if row.get("locality_name") and not row.get("street"):
            row["street"] = row.get("locality_name")

        # ✅ phone clean
        phone = (row.get("phone") or "").strip()
        row["phone"] = phone.replace(" ", "") if phone else ""

        # ✅ City mapping
        city_text = (row.get("city_text") or "").strip()

        if city_text:
            city_obj = self.get_city_obj(city_text)
            if city_obj:
                row["city"] = city_obj.id
        else:
            fallback_city = self.get_city_obj("Unknown")
            if fallback_city:
                row["city"] = fallback_city.id
            row["city_text"] = "Unknown"

        # ✅ category mapping
        cat_text = (row.get("category_text") or "").strip()
        if cat_text:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_text)
            row["category"] = cat_obj.id

        # ✅ locality mapping
        loc_name = (row.get("street") or row.get("address") or "").strip()
        if loc_name and len(loc_name) > 2 and row.get("city"):
            locality_obj, _ = Locality.objects.get_or_create(
                locality_name=loc_name[:200],
                city_id=row.get("city")
            )
            row["locality"] = locality_obj.id
