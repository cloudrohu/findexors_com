from import_export import resources
from .models import GoogleCompany
from utility.models import City, Category


class GoogleCompanyResource(resources.ModelResource):

    class Meta:
        model = GoogleCompany
        import_id_fields = ("place_id",)
        skip_unchanged = True
        report_skipped = True

        # ✅ IMPORTANT: FK fields "category" & "city" ko import list se hata diya
        fields = (
            "id", "name", "name_for_emails",

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

    # ✅ City field auto detect
    def get_city_obj(self, city_name):
        possible_fields = ["city_name", "name", "title", "city"]
        model_fields = [f.name for f in City._meta.fields]

        for f in possible_fields:
            if f in model_fields:
                obj, _ = City.objects.get_or_create(**{f: city_name})
                return obj
        return None

    def before_import_row(self, row, **kwargs):

        # ✅ normalize csv headers
        if row.get("city_name") and not row.get("city_text"):
            row["city_text"] = row.get("city_name")

        if row.get("category_name") and not row.get("category_text"):
            row["category_text"] = row.get("category_name")

        # ✅ Clean phone
        phone = (row.get("phone") or "").strip()
        row["phone"] = phone.replace(" ", "") if phone else ""

    def after_import_instance(self, instance, new, row_number=None, **kwargs):
        """
        ✅ FK mapping import ke baad, validation error nahi aayega.
        """

        # ----------------------------
        # ✅ City mapping
        # ----------------------------
        city_text = (instance.city_text or "").strip()
        if city_text:
            city_obj = self.get_city_obj(city_text)
            if city_obj:
                instance.city = city_obj

        # ----------------------------
        # ✅ Category mapping
        # ----------------------------
        cat_text = (instance.category_text or "").strip()
        if cat_text:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_text)
            instance.category = cat_obj

        instance.save()
