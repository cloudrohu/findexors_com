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
        """✅ Auto detect city field"""
        possible_fields = ["city_name", "name", "title", "city"]
        model_fields = [f.name for f in City._meta.fields]

        for f in possible_fields:
            if f in model_fields:
                obj, _ = City.objects.get_or_create(**{f: city_name})
                return obj
        return None

    def get_locality_obj(self, locality_title, city_id=None):
        """✅ Auto detect Locality name field"""
        possible_fields = ["locality_name", "name", "title", "locality"]
        model_fields = [f.name for f in Locality._meta.fields]

        create_data = {}
        for f in possible_fields:
            if f in model_fields:
                create_data[f] = locality_title
                break

        # ✅ agar koi matching field hi nahi mila
        if not create_data:
            return None

        # ✅ if Locality has FK city
        if city_id and "city" in model_fields:
            create_data["city_id"] = city_id

        obj, _ = Locality.objects.get_or_create(**create_data)
        return obj

    def before_import_row(self, row, **kwargs):

        # ✅ normalize csv headers
        if row.get("city_name") and not row.get("city_text"):
            row["city_text"] = row.get("city_name")

        if row.get("category_name") and not row.get("category_text"):
            row["category_text"] = row.get("category_name")

        if row.get("locality_name") and not row.get("street"):
            row["street"] = row.get("locality_name")

        # ✅ phone clean
        phone = (row.get("phone") or "").strip()
        row["phone"] = phone.replace(" ", "") if phone else ""

        # ✅ CITY mapping
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

        # ✅ CATEGORY mapping
        cat_text = (row.get("category_text") or "").strip()
        if cat_text:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_text)
            row["category"] = cat_obj.id

        # ✅ LOCALITY mapping
        loc_name = (row.get("street") or row.get("address") or "").strip()
        if loc_name and len(loc_name) > 2 and row.get("city"):
            locality_obj = self.get_locality_obj(loc_name[:200], city_id=row.get("city"))
            if locality_obj:
                row["locality"] = locality_obj.id
