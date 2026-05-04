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


class Response(models.Model):

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
        ("instagram", "Instagram Ads"),
        ("facebook", "Facebook Ads"),
        ("google", "Google Ads"),
        ("website", "Website"),
        ("whatsapp", "WhatsApp"),
        ("Just Dial", "Just Dial"),
        ("manual", "Manual"),
    ]

    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        default="manual",
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
        "response.Staff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_responses"
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
        related_name="responses"
    )

    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    locality = models.ForeignKey(Locality, blank=True, null=True, on_delete=models.SET_NULL)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="responses_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="responses_updated",
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
        verbose_name_plural = "0. Responses"
        indexes = [
            models.Index(fields=["contact_no"]),
            models.Index(fields=["status"]),
        ]


class Meeting(models.Model):

    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="meetings"
    )

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES
    )

    meeting_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        "response.Staff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="meeting_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="meeting_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If deal done → auto convert lead
        if self.status == "Deal Done":
            self.response.is_converted = True
            self.response.save()

    def __str__(self):
        return f"Meeting {self.id} - {self.status}"

    class Meta:
        ordering = ["-meeting_date"]




class Followup(models.Model):

    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="followups"
    )

    status = models.CharField(max_length=25, choices=FOLLOWUP_STATUS_CHOICES)

    followup_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        "response.Staff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="followup_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="followup_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == "Deal Done":
            self.response.is_converted = True
            self.response.save()

    class Meta:
        ordering = ["-followup_date"]

# =======================
#  Comment
# =======================
class Comment(models.Model):
    response = models.ForeignKey(
        Response,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    comment = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='comments_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name='comments_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"


# =======================
#  Voice Recording
# =======================
class VoiceRecording(models.Model):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='recordings'
    )

    file = models.FileField(upload_to='voice_recordings/')
    note = models.CharField(max_length=255, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Recording {self.id} - {self.file.name}"
