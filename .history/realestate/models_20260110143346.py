from django.db import models
from django.contrib.auth.models import User
from response.models import Staff


# ============================================================
# GOOGLE COMPANY MODEL (Outscraper)
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

    place_id = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    cid = models.CharField(max_length=255, blank=True, null=True)

    business_status = models.CharField(max_length=255, blank=True, null=True)
    working_hours = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    logo = models.URLField(blank=True, null=True)  # Outscraper logo url

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "0. Google Companies"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# ============================================================
# COMMENT MODEL
# ============================================================
class Comment(models.Model):
    company = models.ForeignKey(
        GoogleCompany,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_comment_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_comment_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - Comment {self.id}"


# ============================================================
# VOICE RECORDING MODEL
# ============================================================
class VoiceRecording(models.Model):
    company = models.ForeignKey(
        GoogleCompany,
        on_delete=models.CASCADE,
        related_name="voice_recordings"
    )

    file = models.FileField(upload_to="call_recordings/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        User,
        related_name="realestate_voice_uploaded",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - Voice {self.id}"


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

    company = models.ForeignKey(
        GoogleCompany,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    visit_for = models.CharField(max_length=50, choices=VISIT_FOR_CHOICES)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    visit_status = models.CharField(max_length=50, choices=VISIT_STATUS_CHOICES)

    comment = models.TextField(max_length=1000, blank=True, null=True)

    uploaded_by = models.ForeignKey(
        User,
        related_name="realestate_visit_uploaded_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.visit_type}"


# ============================================================
# FOLLOWUP MODEL (OneToOne)
# ============================================================
class Followup(models.Model):
    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(
        GoogleCompany,
        on_delete=models.CASCADE,
        related_name="followup"
    )

    status = models.CharField(max_length=25, choices=FOLLOWUP_STATUS_CHOICES)
    followup_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        Staff,
        related_name="realestate_followup_assigned",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_followup_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_followup_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.status}"


# ============================================================
# MEETING MODEL (OneToOne)
# ============================================================
class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    company = models.OneToOneField(
        GoogleCompany,
        on_delete=models.CASCADE,
        related_name="meeting"
    )

    status = models.CharField(max_length=25, choices=MEETING_STATUS_CHOICES)
    meeting_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        Staff,
        related_name="realestate_meeting_assigned",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comment = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="realestate_meeting_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="realestate_meeting_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.status}"
