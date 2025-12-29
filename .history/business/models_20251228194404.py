from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify

from utility.models import (
    SocialSite, Googlemap_Status,
    City, Locality, Category, Sub_Locality
)
from response.models import Staff


# ============================================================
# COMPANY
# ============================================================
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

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, blank=True)
    sub_locality = models.ForeignKey(Sub_Locality, on_delete=models.SET_NULL, null=True, blank=True)

    address = models.CharField(max_length=500, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)

    contact_no = models.CharField(max_length=50, blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    google_map = models.URLField(blank=True, null=True)
    googlemap_status = models.ForeignKey(Googlemap_Status, on_delete=models.SET_NULL, null=True, blank=True)

    logo = models.ImageField(upload_to="company/logo/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    total_reviews = models.PositiveIntegerField(default=0)

    slug = models.SlugField(max_length=500, blank=True, null=True)

    created_by = models.ForeignKey(User, related_name="company_created", on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="company_updated", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "1. Companies"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = f"{slugify(self.company_name)}-{self.id}"
            super().save(update_fields=["slug"])

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"slug": self.slug})

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="60"/>')
        return "No Image"


# ============================================================
# IMAGES (🔥 FIXED)
# ============================================================
class Images(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="company/images/")

    def __str__(self):
        return self.title or "Image"


# ============================================================
# COMMENT
# ============================================================
class Comment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:30]


# ============================================================
# VOICE RECORDING
# ============================================================
class VoiceRecording(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="voice_recordings")
    file = models.FileField(upload_to="call_recordings/")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording {self.id}"


# ============================================================
# VISIT
# ============================================================
class Visit(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="visits")
    visit_type = models.CharField(max_length=50)
    visit_status = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.visit_type}"


# ============================================================
# FAQ
# ============================================================
class Faq(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question
