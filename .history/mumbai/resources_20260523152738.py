from import_export import resources
from .models import MumbaiRealEstateGMB,Refrense
from utility.models import City, Category, Locality, Sub_Locality



class MumbaiRealEstateGMBResource(resources.ModelResource):

    class Meta:
        model = MumbaiRealEstateGMB
        import_id_fields = ("place_id",)
        skip_unchanged = True
        report_skipped = True

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

    # =========================
    # 🔥 CITY DETECT (same logic)
    # =========================
    def get_city_obj(self, city_name):
        possible_fields = ["city_name", "name", "title", "city"]
        model_fields = [f.name for f in City._meta.fields]

        for f in possible_fields:
            if f in model_fields:
                obj, _ = City.objects.get_or_create(**{f: city_name})
                return obj
        return None

    # =========================
    # 🔥 BEFORE IMPORT
    # =========================
    def before_import_row(self, row, **kwargs):

        # ✅ normalize headers
        if row.get("city_name") and not row.get("city_text"):
            row["city_text"] = row.get("city_name")

        if row.get("category_name") and not row.get("category_text"):
            row["category_text"] = row.get("category_name")

        # ✅ clean phone
        phone = (row.get("phone") or "").strip()
        row["phone"] = phone.replace(" ", "") if phone else ""

    # =========================
    # 🔥 AFTER IMPORT (FK MAPPING)
    # =========================
    def after_import_instance(self, instance, new, row_number=None, **kwargs):

        # -------------------
        # CITY
        # -------------------
        city_text = (instance.city_text or "").strip()
        if city_text:
            city_obj = self.get_city_obj(city_text)
            if city_obj:
                instance.city = city_obj

        # -------------------
        # CATEGORY
        # -------------------
        cat_text = (instance.category_text or "").strip()
        if cat_text:
            cat_obj, _ = Category.objects.get_or_create(category_name=cat_text)
            instance.category = cat_obj

        # -------------------
        # LOCALITY (optional 🔥)
        # -------------------
        if instance.locality and instance.city:
            instance.locality.city = instance.city

        instance.save()







class RefrenseResource(resources.ModelResource):

    class Meta:

        model = Refrense

        import_id_fields = ("contact_no",)

        skip_unchanged = True
        report_skipped = True

        fields = (

            "id",

            "refrense_name",

            "status",

            "category",

            "contact_no",
            "email",
            "website",

            "address",

            "description",

            "rating",
            "reviews_count",

            "business_status_raw",

            "google_map",

            "created_at",
            "updated_at",
        )

    # =========================================
    # ✅ CITY GETTER
    # =========================================

    def get_city_obj(self, city_name):

        possible_fields = [
            "city_name",
            "name",
            "title",
            "city"
        ]

        model_fields = [
            f.name for f in City._meta.fields
        ]

        for f in possible_fields:

            if f in model_fields:

                obj, _ = City.objects.get_or_create(
                    **{f: city_name}
                )

                return obj

        return None

    # =========================================
    # ✅ BEFORE IMPORT
    # =========================================

    def before_import_row(self, row, **kwargs):

        # =====================================
        # CLEAN PHONE
        # =====================================

        phone = (row.get("contact_no") or "").strip()

        row["contact_no"] = (
            phone.replace(" ", "")
            .replace("-", "")
            .replace("+91", "")
        )

        # =====================================
        # CLEAN EMAIL
        # =====================================

        if row.get("email"):

            row["email"] = (
                row.get("email")
                .strip()
                .lower()
            )

        # =====================================
        # DEFAULT STATUS
        # =====================================

        if not row.get("status"):

            row["status"] = "New"

    # =========================================
    # ✅ AFTER IMPORT
    # =========================================

    def after_import_instance(
        self,
        instance,
        new,
        row_number=None,
        **kwargs
    ):

        # =====================================
        # CATEGORY
        # =====================================

        category_name = kwargs.get("row", {}).get("category")

        if category_name:

            category_obj, _ = Category.objects.get_or_create(
                category_name=category_name
            )

            instance.category = category_obj

        # =====================================
        # SAVE
        # =====================================

        instance.save()