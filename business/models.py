from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q

# Utility aur Response app ke imports
from utility.models import (
    Find_Form, Call_Status, SocialSite, Googlemap_Status,
    City, Locality, Category, Sub_Locality
)
from response.models import Staff
from properties.models import Project 

# ============================================================
# COMPANY MODEL
# ============================================================

class GoogleCompany(models.Model):
    name = models.CharField(max_length=255)
    name_for_emails = models.CharField(max_length=255, blank=True, null=True)

    category_text = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    phone = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    website = models.URLField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)

    city_text = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)

    place_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    cid = models.CharField(max_length=255, blank=True, null=True)

    business_status = models.CharField(max_length=255, blank=True, null=True)
    working_hours = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    logo = models.URLField(blank=True, null=True)   # outscraper logo url

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "0. Google Companies"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name






class Company(models.Model):

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
    ]

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="New")
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    company_name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # 👇 CHANGE: City aur Locality ab Required hain (Mandatory)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
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

    created_by = models.ForeignKey(User, related_name="company_created", on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="company_updated", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Company"
        verbose_name_plural = "1. Company"


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

  



# ============================================================
# COMMENT MODEL
# ============================================================
class Comment(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='business_comments_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='business_comments_updated', on_delete=models.SET_NULL, null=True, blank=True)



    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"


# ============================================================
# VOICE RECORDING MODEL
# ============================================================
class VoiceRecording(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='voice_recordings')
    file = models.FileField(upload_to='call_recordings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='business_voice_uploaded', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Voice Recording for {self.company} ({self.uploaded_at.strftime('%d-%m-%Y %H:%M')})"


# ============================================================
# VISIT MODEL
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
        ("1st Visit", "1st Visit"), ("2nd Visit", "2nd Visit"), ("3rd Visit", "3rd Visit"),
        ("4th Visit", "4th Visit"), ("5th Visit", "5th Visit"), ("6th Visit", "6th Visit"),
        ("7th Visit", "7th Visit"), ("8th Visit", "8th Visit"), ("9th Visit", "9th Visit"),
        ("10th Visit", "10th Visit"),
    ]

    VISIT_STATUS_CHOICES = [
        ("Deal_Close", "Deal Close"), ("Meeting", "Meeting"), ("Follow_Up", "Follow Up"),
        ("Owner not In Office", "Owner not In Office"), ("Interested", "Interested"),
        ("Not Interested", "Not Interested"),
    ]

    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="visits")
    visit_for = models.CharField(max_length=50, choices=VISIT_FOR_CHOICES)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    visit_status = models.CharField(max_length=50, choices=VISIT_STATUS_CHOICES)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, related_name="visits_uploaded_by", on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.company.company_name} - {self.visit_type} ({self.visit_status})"


# ============================================================
# APPROX MODEL
# ============================================================
class Approx(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ============================================================
# SOCIAL LINK MODEL
# ============================================================
class SocialLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    social_site = models.ForeignKey(SocialSite, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=50, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link


# ============================================================
# ERROR MODEL
# ============================================================
class Error(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500, unique=True)
    error = models.CharField(max_length=500, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ============================================================
# IMAGES MODEL
# ============================================================
class Images(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title


# ============================================================
# FAQ MODEL
# ============================================================
class Faq(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    questions = models.CharField(max_length=500, blank=True)
    answers = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questions


# ============================================================
# FOLLOWUP MODEL (FINAL)
# ============================================================
class Followup(models.Model):

    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="followup"
    )

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        verbose_name="Followup Status"
    )

    followup_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Followup Date & Time"
    )

    assigned_to = models.ForeignKey(
        Staff,
        related_name='business_followup_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='business_followup_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name='business_followup_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company} - {self.status}"

class Meeting(models.Model):

    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="meeting"
    )

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        verbose_name="Meeting Status"
    )

    meeting_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Meeting Date & Time"
    )

    assigned_to = models.ForeignKey(
        Staff,
        related_name='business_meeting_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='business_meeting_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='business_meeting_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company} - {self.status}"
