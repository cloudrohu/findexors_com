import re
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
# Utility aur Response app ke imports




from utility.models import (
    Find_Form, Call_Status, SocialSite, Googlemap_Status,
    City, Locality, Category, Sub_Locality,RequirementType
)

from response.models import Staff
from projects.models import Project  # Project Import

def clean_phone_last10(phone: str):
    if not phone:
        return None

    digits = re.sub(r"\D", "", str(phone))
    return digits[-10:] if len(digits) >= 10 else digits


# =======================
# Staff
# =======================
class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username



class MumbaiCompany(models.Model):
    STATUS_CHOICES = [
    ("New", "New"),
    ("Meeting", "Meeting"),
    ("FollowUp", "Follow Up"),
    ("Not_received", "Not Received"),
    ("Not Interested", "Not Interested"),
    ("They Will Connect", "They Will Connect"),
    ("Call later", "Call later"),
    ("Call Tomorrow", "Call Tomorrow"),
    ("Switched Off", "Switched Off"),
    ("Invalid Number", "Invalid Number"),
    ("Meeting_FollowUp", "Meeting-Follow Up"),
]



    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="New")
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    company_name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # 👇 CHANGE: City aur Locality ab Required hain (Mandatory)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,null=True, blank=True)
    
    # Sub-locality aur Project Optional rakh sakte hain
    sub_locality = models.ForeignKey(Sub_Locality, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    address = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    # 👇 CHANGE: unique=True for Number
    contact_no = models.CharField(
    max_length=50,
    unique=True,
    blank=True,
    null=True
)
    
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    google_map = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )

    reviews_count = models.IntegerField(null=True, blank=True)

    business_status_raw = models.CharField( max_length=50,null=True,blank=True)
    
    
    googlemap_status = models.ForeignKey(Googlemap_Status, on_delete=models.SET_NULL, null=True, blank=True)

    logo = models.ImageField(upload_to="company/logo/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(max_length=500, blank=True, null=True)

    created_by = models.ForeignKey(User, related_name="MumbaiCompany_created", on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="MumbaiCompany_updated", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mumbai Company"
        verbose_name_plural = "1. Mumbai Company"


    def __str__(self):
        return self.company_name


    def save(self, *args, **kwargs):
        # ✅ Phone number clean
        if self.contact_no:
            self.contact_no = self.contact_no.replace(" ", "").strip()

        # ✅ First save (to get ID)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # ✅ Slug generate ONLY once, AFTER ID exists
        if is_new and not self.slug:
            self.slug = f"{slugify(self.company_name)}-{self.id}"
            super().save(update_fields=["slug"])


    def logo_preview(self):
        if self.logo:
            return mark_safe(
                f'<img src="{self.logo.url}" width="60" style="border-radius:6px;" />'
            )
        return "No Image"

    logo_preview.short_description = "Logo"
# =======================
# MumbaiResponse
# =======================
class MumbaiResponse(models.Model):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Not_received", "Not Received"),
        ("Software_company", "Software Company"),
        ("For_job", "For Job"),
        ("Training", "Training"),
        ("Fake_lead", "Fake Lead"),
        ("Deal_close", "Deal Close"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
    ]

    LEAD_SOURCE_CHOICES = [
        ("meta", "Meta Ads"),
        ("google", "Google Ads"),
        ("website", "Website"),
        ("whatsapp", "WhatsApp"),
        ("Just Dial", "Just Dial"),
        ("manual", "Manual"),
    ]

    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        default="meta"
    )

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New"
    )

    contact_no = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_assigned_responses"
    )

    contact_persone = models.CharField(max_length=500, blank=True, null=True)

    business_name = models.CharField(max_length=500, blank=True, null=True)

    business_category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name="mumbai_requirements"
    )

    locality = models.ForeignKey(
        Locality,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    comment = models.TextField(null=True, blank=True)

    whatsapp_welcome_sent = models.BooleanField(default=False)
    whatsapp_followup_1_sent = models.BooleanField(default=False)
    whatsapp_followup_2_sent = models.BooleanField(default=False)

    is_converted = models.BooleanField(default=False)

    converted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_created_responses"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_updated_responses"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-create_at"]

    def __str__(self):
        return f"MR{str(self.id).zfill(3)} - {self.contact_no or 'No Number'}"

    def save(self, *args, **kwargs):

        # ✅ clean phone
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        # ✅ converted date
        if self.is_converted and not self.converted_at:
            self.converted_at = timezone.now()

        if not self.is_converted:
            self.converted_at = None

        super().save(*args, **kwargs)


class MumbaiRealEstateGMB(models.Model):
    name = models.CharField(max_length=255)
    name_for_emails = models.CharField(max_length=255, blank=True, null=True)

    # ===========================
    # ✅ SAFE FOREIGN KEYS (NO CLASH)
    # ===========================

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_categories"
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_cities"
    )

    locality = models.ForeignKey(
        Locality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_localities"
    )

    sub_locality = models.ForeignKey(
        Sub_Locality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_sublocalities"
    )

    # ===========================
    # BASIC INFO
    # ===========================

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

    STATUS_CHOICES = [
    ("New", "New"),
    ("Meeting", "Meeting"),
    ("FollowUp", "Follow Up"),
    ("Call_Cut", "Call Cut"),
    ("Not Received", "Not Received"),
    ("Not Interested", "Not Interested"),
    ("Deal Done", "Deal Done"),
    ("Meeting_FollowUp", "Meeting-Follow Up"),
]

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="New")

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_assigned"
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(max_length=500, blank=True, null=True, db_index=True)

    # ===========================
    # ✅ FIXED USER FIELDS (NO CLASH)
    # ===========================

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_gmb_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "0.Real Estate"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.city_text})"



class Comment(models.Model):

    FORM_CHOICES = [
        ("Response", "Response"),
        ("Company", "Company"),
        ("Real_Estate", "Real Estate"),

    ]

    form_type = models.CharField(
    max_length=20,
    choices=FORM_CHOICES,
    default="Response"   # 🔥 IMPORTANT
)

    response = models.ForeignKey(
        "MumbaiResponse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    company = models.ForeignKey(
        "MumbaiCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    real_estate = models.ForeignKey(
        "MumbaiRealEstateGMB",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    # 🔥 ADD THESE
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)# =======================


class VoiceRecording(models.Model):

    FORM_CHOICES = [
        ("Response", "Response"),
        ("Company", "Company"),
        ("Real_Estate", "Real Estate"),

    ]

    form_type = models.CharField(
        max_length=20,
        choices=FORM_CHOICES,
        default="Response"
    )

    response = models.ForeignKey(
        "MumbaiResponse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings"
    )

    company = models.ForeignKey(
        "MumbaiCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings"
    )

    real_estate = models.ForeignKey(
        "MumbaiRealEstateGMB",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voices"
    )

    file = models.FileField(upload_to="call_recordings/")

    # 🔥 UNIQUE related_name (IMPORTANT FIX)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_voice_uploaded"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form_type} Voice {self.id}"

    # ✅ VALIDATION
    def clean(self):
        if self.form_type == "Response" and not self.response:
            raise ValidationError("Response required")

        if self.form_type == "Company" and not self.company:
            raise ValidationError("Company required")

    # ✅ SAFE SAVE
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Visit(models.Model):

    FORM_CHOICES = [
        ("Response", "Response"),
        ("Company", "Company"),
        ("Real_Estate", "Real Estate"),

    ]

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

    # 🔥 MAIN CONTROL FIELD
    form_type = models.CharField(
        max_length=20,
        choices=FORM_CHOICES,
        default="Response"
    )

    # 🔥 BOTH LINKS (IMPORTANT)
    response = models.ForeignKey(
        "MumbaiResponse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits"
    )

    company = models.ForeignKey(
        "MumbaiCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits"
    )

    real_estate = models.ForeignKey(
        "MumbaiRealEstateGMB",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits"
    )

    visit_for = models.CharField(max_length=50, choices=VISIT_FOR_CHOICES)
    
    
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    visit_status = models.CharField(max_length=50, choices=VISIT_STATUS_CHOICES)

    comment = models.TextField(null=True, blank=True)

    # 🔥 TRACKING
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visit_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form_type} Visit {self.id}"

    # 🔥 VALIDATION (MOST IMPORTANT)
    def clean(self):
        if self.form_type == "Response" and not self.response:
            raise ValidationError("Response required")

        if self.form_type == "Company" and not self.company:
            raise ValidationError("Company required")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
# =======================
# Followup
# =======================
class Followup(models.Model):

    FORM_CHOICES = [
        ("Response", "Response"),
        ("Company", "Company"),
        ("Real_Estate", "Real Estate"),
    ]

    FOLLOWUP_FROM_CHOICES = [
        ("Response", "Response"),
        ("Door_To_Door", "Door_To_Door"),
        ("Data_Calling", "Data_Calling"),
    ]

    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    # =====================================
    # AUTO TYPE
    # =====================================

    form_type = models.CharField(
        max_length=20,
        choices=FORM_CHOICES,
        default="Response"
    )

    # =====================================
    # LINKS
    # =====================================

    response = models.OneToOneField(
        "MumbaiResponse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup"
    )

    company = models.OneToOneField(
        "MumbaiCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup"
    )

    real_estate = models.OneToOneField(
        "MumbaiRealEstateGMB",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup"
    )

    # =====================================
    # STATUS
    # =====================================

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        default="New Followup"
    )

    followup_from = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=FOLLOWUP_FROM_CHOICES
    )

    followup_date = models.DateTimeField(
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="followup_assigned"
    )

    comment = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    # =====================================
    # TRACKING
    # =====================================

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_followup_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # =====================================
    # STRING
    # =====================================

    def __str__(self):
        return f"{self.form_type} Followup {self.id}"

    # =====================================
    # VALIDATION
    # =====================================

    def clean(self):

        total_links = sum([
            bool(self.response),
            bool(self.company),
            bool(self.real_estate),
        ])

        # ✅ Only one allowed
        if total_links > 1:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                "Only one link allowed: Response, Company or Real Estate."
            )

    # =====================================
    # SAVE
    # =====================================

    def save(self, *args, **kwargs):

        # ✅ AUTO DETECT FORM TYPE

        if self.response:
            self.form_type = "Response"

        elif self.company:
            self.form_type = "Company"

        elif self.real_estate:
            self.form_type = "Real_Estate"

        self.full_clean()

        super().save(*args, **kwargs)


    # 🔥 VALIDATION
    def clean(self):

        if self.form_type == "Response" and not self.response_id:
            return

        if self.form_type == "Company" and not self.company_id:
            return

        if self.form_type == "Real_Estate" and not self.real_estate_id:
            return
        


class Meeting(models.Model):

    FORM_CHOICES = [
        ("Response", "Response"),
        ("Company", "Company"),
        ("Real_Estate", "Real Estate"),
    ]

    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    # =========================================
    # FORM TYPE
    # =========================================

    form_type = models.CharField(
        max_length=20,
        choices=FORM_CHOICES,
        default="Response"
    )

    # =========================================
    # LINKS
    # =========================================

    response = models.OneToOneField(
        "MumbaiResponse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting"
    )

    company = models.OneToOneField(
        "MumbaiCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting"
    )

    real_estate = models.OneToOneField(
        "MumbaiRealEstateGMB",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting"
    )

    # =========================================
    # DETAILS
    # =========================================

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        default="New Meeting"
    )

    meeting_date = models.DateTimeField(
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_staff_meetings"
    )

    comment = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    # =========================================
    # TRACKING
    # =========================================

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_user_created_meetings"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mumbai_user_updated_meetings"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # =========================================
    # STRING
    # =========================================

    def __str__(self):
        return f"{self.form_type} Meeting {self.id}"

    # =========================================
    # VALIDATION
    # =========================================

    def clean(self):

        total = sum([
            bool(self.response),
            bool(self.company),
            bool(self.real_estate),
        ])

        # ✅ MINIMUM ONE REQUIRED

        if total == 0:
            raise ValidationError(
                "Please select Response, Company or Real Estate."
            )

        # ✅ ONLY ONE ALLOWED

        if total > 1:
            raise ValidationError(
                "Only one field allowed: Response, Company or Real Estate."
            )

    # =========================================
    # SAVE
    # =========================================

    def save(self, *args, **kwargs):

        # ✅ AUTO FORM TYPE

        if self.response:
            self.form_type = "Response"

        elif self.company:
            self.form_type = "Company"

        elif self.real_estate:
            self.form_type = "Real_Estate"

        self.full_clean()

        super().save(*args, **kwargs)