from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import mark_safe

from response.models import Staff
from utility.models import (
    City, Locality, Category, Sub_Locality
)
from projects.models import Project


class GoogleCompany(models.Model):
    name = models.CharField(max_length=255)
    name_for_emails = models.CharField(max_length=255, blank=True, null=True)

    # ✅ FK mapping (optional for import safety)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, blank=True)
    sub_locality = models.ForeignKey(Sub_Locality, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    # ✅ original text fields (Outscraper)
    category_text = models.CharField(max_length=550, blank=True, null=True, db_index=True)
    type = models.CharField(max_length=550, blank=True, null=True, db_index=True)

    phone = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    website = models.CharField(max_length=550, blank=True, null=True, db_index=True)

    address = models.CharField(max_length=550, blank=True, null=True, db_index=True)
    street = models.CharField(max_length=550, blank=True, null=True, db_index=True)

    city_text = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    state = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    country = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)

    place_id = models.CharField(max_length=300, blank=True, null=True, unique=True, db_index=True)
    google_id = models.CharField(max_length=300, blank=True, null=True, db_index=True)
    cid = models.CharField(max_length=300, blank=True, null=True, db_index=True)

    business_status = models.CharField(max_length=550, blank=True, null=True, db_index=True)
    working_hours = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    logo = models.URLField(blank=True, null=True)

    # ✅ CRM fields
    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Not_received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("They Will Connect", "They Will Connect"),
        ("Call later", "Call later"),
        ("Call Tomorrow", "Call Tomorrow"),
        ("Switched Off", "Switched Off"),
        ("Invalid Number", "Invalid Number"),
        ("Send Ditails", "Send Ditails"),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="New")

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="realestate_googlecompany_assigned"
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(max_length=500, blank=True, null=True, db_index=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_googlecompany_created",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_googlecompany_updated",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


    class Meta:
        verbose_name_plural = "0. Google Companies"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.city_text})"

    def save(self, *args, **kwargs):
        # ✅ Phone clean
        if self.phone:
            self.phone = self.phone.replace(" ", "").strip()

        super().save(*args, **kwargs)

        # ✅ stable slug
        expected_slug = f"{slugify(self.name)}-{self.id}"
        if self.slug != expected_slug:
            self.slug = expected_slug
            super().save(update_fields=["slug"])

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<a href="{self.logo}" target="_blank">View Logo</a>')
        return "No Logo"

    logo_preview.short_description = "Logo"


# ============================================================
# COMMENT MODEL
# ============================================================
class Comment(models.Model):
    company = models.ForeignKey(GoogleCompany, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_comment_created",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_comment_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.company.name} - Comment {self.id}"


# ============================================================
# VOICE
# ============================================================
class VoiceRecording(models.Model):
    company = models.ForeignKey(GoogleCompany, on_delete=models.CASCADE, related_name="voice_recordings")
    file = models.FileField(upload_to="call_recordings/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        User,
        related_name="realestate_voice_uploaded",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.company.name} - Voice {self.id}"


# ============================================================
# VISIT
# ============================================================
class Visit(models.Model):
    VISIT_FOR_CHOICES = [
        ("Telling Meeting", "Telling Meeting"),
        ("Door To Door", "Door To Door"),
        ("Site Visit", "Site Visit"),
        ("Follow Up", "Follow Up"),
        ("Negotiation", "Negotiation"),
    ]
    VISIT_TYPE_CHOICES = [
        ("1st Visit", "1st Visit"),
        ("2nd Visit", "2nd Visit"),
        ("3rd Visit", "3rd Visit"),
        ("4th Visit", "4th Visit"),
        ("5th Visit", "5th Visit"),
    ]
    VISIT_STATUS_CHOICES = [
        ("Deal_Close", "Deal Close"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Owner not In Office", "Owner not In Office"),
        ("Interested", "Interested"),
        ("Not Interested", "Not Interested"),
    ]

    company = models.ForeignKey(GoogleCompany, on_delete=models.CASCADE, related_name="visits")
    visit_for = models.CharField(max_length=50, choices=VISIT_FOR_CHOICES)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    visit_status = models.CharField(max_length=50, choices=VISIT_STATUS_CHOICES)

    comment = models.TextField(max_length=1000, blank=True, null=True)

    uploaded_by = models.ForeignKey(
        User,
        related_name="realestate_visit_uploaded_by",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.visit_type}"


# ============================================================
# FOLLOWUP
# ============================================================
class Followup(models.Model):
    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(GoogleCompany, on_delete=models.CASCADE, related_name="followup")
    status = models.CharField(max_length=25, choices=FOLLOWUP_STATUS_CHOICES)
    followup_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        Staff,
        related_name="realestate_followup_assigned",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_followup_created",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_followup_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.status}"


# ============================================================
# MEETING
# ============================================================
class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(GoogleCompany, on_delete=models.CASCADE, related_name="meeting")
    status = models.CharField(max_length=25, choices=MEETING_STATUS_CHOICES)
    meeting_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        Staff,
        related_name="realestate_meeting_assigned",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_meeting_created",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_meeting_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.status}"
