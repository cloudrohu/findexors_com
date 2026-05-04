import re
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utility.models import Category, City, Locality, RequirementType


# =======================
# Phone Cleaner
# =======================
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


# =======================
# AhmedabadResponse
# =======================
class AhmedabadResponse(models.Model):

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

    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default="meta")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="New")

    contact_no = models.CharField(max_length=16, unique=True, null=True, blank=True)

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_assigned_responses"
    )

    contact_persone = models.CharField(max_length=500, blank=True, null=True)
    business_name = models.CharField(max_length=500, blank=True, null=True)

    business_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name="ahmedabad_requirements"
    )

    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    locality = models.ForeignKey(Locality, null=True, blank=True, on_delete=models.SET_NULL)

    whatsapp_welcome_sent = models.BooleanField(default=False)
    whatsapp_followup_1_sent = models.BooleanField(default=False)
    whatsapp_followup_2_sent = models.BooleanField(default=False)

    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_created_responses"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_updated_responses"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        if self.is_converted and not self.converted_at:
            self.converted_at = timezone.now()

        if not self.is_converted:
            self.converted_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"MR{str(self.id).zfill(3)} - {self.contact_no or 'No Number'}"

    class Meta:
        ordering = ["-create_at"]


# =======================
# Comment
# =======================
class Comment(models.Model):
    company = models.ForeignKey(AhmedabadResponse, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_comment_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_comment_updated"
    )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id}"


# =======================
# Voice Recording
# =======================
class VoiceRecording(models.Model):
    company = models.ForeignKey(AhmedabadResponse, on_delete=models.CASCADE, related_name="voice_recordings")
    file = models.FileField(upload_to="call_recordings/")

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_voice_uploaded"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voice {self.id}"


# =======================
# Visit
# =======================
class Visit(models.Model):
    company = models.ForeignKey(AhmedabadResponse, on_delete=models.CASCADE, related_name="visits")

    visit_for = models.CharField(max_length=50)
    visit_type = models.CharField(max_length=50)
    visit_status = models.CharField(max_length=50)

    comment = models.TextField(null=True, blank=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_visit_uploaded"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit {self.id}"


# =======================
# Followup
# =======================
class Followup(models.Model):
    company = models.OneToOneField(AhmedabadResponse, on_delete=models.CASCADE, related_name="followup")

    status = models.CharField(max_length=25)
    followup_date = models.DateTimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_followup_assigned"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_followup_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_followup_updated"
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Followup {self.id}"


# =======================
# Meeting
# =======================
class Meeting(models.Model):
    company = models.OneToOneField(AhmedabadResponse, on_delete=models.CASCADE, related_name="meeting")

    status = models.CharField(max_length=25)
    meeting_date = models.DateTimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_meeting_assigned"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_meeting_created"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ahmedabad_meeting_updated"
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting {self.id}"