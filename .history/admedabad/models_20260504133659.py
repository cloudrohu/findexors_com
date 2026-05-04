from django.db import models

# Create your models here.

import re
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify



from utility.models import Category, City, Locality, RequirementType


# ✅ Phone Cleaner (Save Time): last 10 digits only
def clean_phone_last10(phone: str):
    """
    ✅ Keeps field max_length same (16),
    but when saving returns ONLY last 10 digits.
    Works with +91, spaces, dashes, etc.
    """
    if not phone:
        return None

    phone = str(phone).strip()

    # ✅ keep only digits
    digits = re.sub(r"\D", "", phone)

    # ✅ return last 10 digits if available
    if len(digits) >= 10:
        return digits[-10:]

    return digits


# =======================
#  Staff
# =======================
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class MetaResponse(models.Model):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Not_received", "Not Received"),
        ("Software_company", "Software Company"),
        ("For_job", "For Job"),
        ("Training", "Training"),
        ("Fake_lead", "Fake Lead"),
        ("Deal_close", "Deal Close"),
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
        default="Meta Ads",
        db_index=True
    )

    # WhatsApp Tracking
    whatsapp_welcome_sent = models.BooleanField(default=False)
    whatsapp_followup_1_sent = models.BooleanField(default=False)
    whatsapp_followup_2_sent = models.BooleanField(default=False)

    # Conversion Tracking
    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        db_index=True
    )

    contact_no = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meta_responses_assigned"
    )

    contact_persone = models.CharField(max_length=500, blank=True, null=True)
    business_name = models.CharField(max_length=500, blank=True, null=True)

    business_category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name="MetaResponses"
    )

    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    locality = models.ForeignKey(Locality, blank=True, null=True, on_delete=models.SET_NULL)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="MetaResponses_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="MetaResponses_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        # Phone clean
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        # Auto conversion timestamp
        if self.is_converted and not self.converted_at:
            self.converted_at = timezone.now()

        if not self.is_converted:
            self.converted_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"MR{str(self.id).zfill(3)} - {self.contact_no or 'No Number'}"

    class Meta:
        ordering = ["-create_at"]
        verbose_name_plural = "0. MetaResponses"
        indexes = [
            models.Index(fields=["contact_no"]),
            models.Index(fields=["status"]),
        ]

