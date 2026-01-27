# jobs/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

from business.models import Company
from utility.models import City, Locality
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

    # ===== BASIC =====
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    openings = models.PositiveIntegerField(default=1)

    # ===== TYPE & LOCATION =====
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_location_type = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default="office")

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    # ===== CANDIDATE =====
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    min_experience_months = models.PositiveIntegerField(default=0)
    max_experience_months = models.PositiveIntegerField(default=0)

    # ===== SALARY =====
    salary_type = models.CharField(max_length=30, choices=SALARY_TYPE_CHOICES, default="fixed")
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()

    # ===== TIME =====
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    working_days = models.ForeignKey(WorkingDaysOption, on_delete=models.SET_NULL, null=True, blank=True)

    # ===== TAGS =====
    skills = models.ManyToManyField(JobSkill, blank=True)
    benefits = models.ManyToManyField(JobBenefit, blank=True)
    assets = models.ManyToManyField(JobAsset, blank=True)
    documents = models.ManyToManyField(JobDocument, blank=True)
    languages = models.ManyToManyField(JobLanguageRequirement, blank=True)

    # ===== CONTENT =====
    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)

    # ===== META =====
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        if creating and not self.slug:
            self.slug = slugify(f"{self.company.company_name}-{self.title.name if self.title else 'job'}-{self.id}")
            super().save(update_fields=["slug"])

    def __str__(self):
        return f"{self.title} | {self.company}"
