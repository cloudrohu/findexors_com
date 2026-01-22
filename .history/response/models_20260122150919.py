import re
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from utility.models import Category, City, Locality, RequirementType


# ✅ Phone Cleaner: +91 / 91 / spaces / ::: / multiple numbers safe
def clean_phone_india(phone: str):
    if not phone:
        return None

    phone = str(phone)

    # ✅ Extract all digit groups
    digit_groups = re.findall(r"\d+", phone)

    # ✅ Pick first valid Indian mobile-like number
    for g in digit_groups:
        if len(g) >= 10:
            last10 = g[-10:]
            # Indian mobiles start with 6-9
            if last10[0] in ["6", "7", "8", "9"]:
                return last10

    # ✅ fallback: take last 10 digits from all digits
    digits = re.sub(r"\D", "", phone)
    if len(digits) >= 10:
        return digits[-10:]
    return digits


# =======================
# Staff
# =======================
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# =======================
# Response
# =======================
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

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Response Status"
    )

    # ✅ Always store only 10 digit number
    contact_no = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    contact_persone = models.CharField(max_length=500, blank=True, null=True)

    business_name = models.CharField(max_length=500, blank=True, null=True)
    business_category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name='responses'
    )

    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, blank=True, null=True, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='responses_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='responses_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # ✅ contact number: store only last 10 digits
        if self.contact_no:
            self.contact_no = clean_phone_india(self.contact_no)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"MR{str(self.id).zfill(3)} -- {self.contact_no or 'No Number'}"

    class Meta:
        verbose_name_plural = '0. Responses'


# =======================
# Meeting
# =======================
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
        related_name='meetings'
    )

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        verbose_name="Meeting Status"
    )

    meeting_date = models.DateTimeField(blank=True, null=True, verbose_name="Meeting Date & Time")

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='meeting_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='meeting_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Meeting {self.id} - {self.status}"


# =======================
# Followup
# =======================
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
        related_name='followups'
    )

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        verbose_name="Followup Status"
    )

    followup_date = models.DateTimeField(blank=True, null=True, verbose_name="Followup Date & Time")

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name='followup_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='followup_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Followup {self.id} - {self.status}"


# =======================
# Comment
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
# Voice Recording
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
