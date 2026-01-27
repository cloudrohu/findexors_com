from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

from business.models import Company
from utility.models import City, Locality
from response.models import Staff
from job_utility.models import (
    JobTitle, JobCategory, JobIndustry,
    JobSkill, JobBenefit, JobAsset,
    JobDocument, JobLanguageRequirement,
    WorkingDaysOption
)

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
    ]

    WORK_LOCATION_CHOICES = [
        ("office", "Office"),
        ("field", "Field"),
        ("home", "Work From Home"),
    ]

    GENDER_CHOICES = [
        ("any", "Any"),
        ("male", "Male"),
        ("female", "Female"),
    ]

    SALARY_TYPE_CHOICES = [
        ("fixed", "Fixed"),
        ("fixed_incentive", "Fixed + Incentive"),
        ("commission", "Commission"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("closed", "Closed"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    openings = models.PositiveIntegerField(default=1)

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_location_type = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default="office")

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    min_experience_months = models.PositiveIntegerField(default=0)
    max_experience_months = models.PositiveIntegerField(default=0)

    salary_type = models.CharField(max_length=30, choices=SALARY_TYPE_CHOICES, default="fixed")
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    working_days = models.ForeignKey(WorkingDaysOption, on_delete=models.SET_NULL, null=True, blank=True)

    skills = models.ManyToManyField(JobSkill, blank=True)
    benefits = models.ManyToManyField(JobBenefit, blank=True)
    assets = models.ManyToManyField(JobAsset, blank=True)
    documents = models.ManyToManyField(JobDocument, blank=True)
    languages = models.ManyToManyField(JobLanguageRequirement, blank=True)

    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.company.company_name}-{self.title}-{self.id}")
            super().save(update_fields=["slug"])

    def __str__(self):
        return f"{self.title} | {self.company}"

class JobApplicant(models.Model):

    APPLICATION_STATUS = [
        ("applied", "New Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview Scheduled"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    ]

    APPLY_SOURCE_CHOICES = [
        ("website", "Website"),
        ("whatsapp", "WhatsApp"),
        ("call", "Call"),
        ("admin", "Admin"),
        ("import", "Imported"),
    ]

    NOTICE_PERIOD_CHOICES = [
        ("immediate", "Immediate"),
        ("15_days", "15 Days"),
        ("30_days", "30 Days"),
        ("45_days", "45 Days"),
        ("60_days", "60 Days"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    experience_months = models.PositiveIntegerField(default=0)
    current_company = models.CharField(max_length=150, blank=True)
    current_salary = models.PositiveIntegerField(blank=True, null=True)
    expected_salary = models.PositiveIntegerField(blank=True, null=True)
    notice_period = models.CharField(max_length=20, choices=NOTICE_PERIOD_CHOICES, blank=True)

    expected_joining_date = models.DateField(blank=True, null=True)

    cover_letter = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)

    apply_source = models.CharField(max_length=20, choices=APPLY_SOURCE_CHOICES, default="website")
    allow_whatsapp = models.BooleanField(default=True)

    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default="applied")
    applied_at = models.DateTimeField(default=timezone.now)
    status_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "phone")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.full_name} → {self.job}"


class InterviewSchedule(models.Model):

    INTERVIEW_TYPE_CHOICES = [
        ("telephonic", "Telephonic"),
        ("video", "Video Call"),
        ("face_to_face", "Face to Face"),
    ]

    INTERVIEW_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("rescheduled", "Rescheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]

    applicant = models.OneToOneField(
        JobApplicant,
        on_delete=models.CASCADE,
        related_name="interview"
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    interview_date = models.DateField()
    interview_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)

    meeting_link = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    remarks = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default="scheduled")

    whatsapp_sent = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant.full_name} | {self.status}"
