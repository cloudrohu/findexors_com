# jobs/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
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
        ("office", "Work from Office"),
        ("field", "Field Job"),
        ("home", "Work from Home"),
    ]

    GENDER_CHOICES = [
        ("any", "Any"),
        ("male", "Male"),
        ("female", "Female"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("closed", "Closed"),
    ]

    SALARY_TYPE_CHOICES = [
        ("fixed", "Fixed Salary"),
        ("fixed_incentive", "Fixed + Incentives"),
        ("commission", "Commission Based"),
    ]

    # ===== BASIC =====
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, blank=True)
    openings = models.PositiveIntegerField(default=1)

    # ===== TYPE =====
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_location_type = models.CharField(
        max_length=20, choices=WORK_LOCATION_CHOICES, blank=True, null=True
    )
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)

    # ===== LOCATION =====
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    # ===== CANDIDATE =====
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    min_experience_months = models.PositiveIntegerField(default=0)
    max_experience_months = models.PositiveIntegerField(default=0)
    only_fresher = models.BooleanField(default=False)

    # ===== SALARY =====
    salary_type = models.CharField(max_length=30, choices=SALARY_TYPE_CHOICES)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()

    # ===== TIMING =====
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    working_days = models.ForeignKey(
        WorkingDaysOption, on_delete=models.SET_NULL, null=True, blank=True
    )

    # ===== TAGS =====
    skills = models.ManyToManyField(JobSkill, blank=True)
    benefits = models.ManyToManyField(JobBenefit, blank=True)
    assets = models.ManyToManyField(JobAsset, blank=True)
    documents = models.ManyToManyField(JobDocument, blank=True)
    languages = models.ManyToManyField(JobLanguageRequirement, blank=True)

    # ===== DESCRIPTION =====
    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)

    # ===== META =====
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ===== VALIDATION =====
    def clean(self):
        if self.salary_min > self.salary_max:
            raise ValidationError("Salary min cannot be greater than salary max.")
        if self.min_experience_months > self.max_experience_months:
            raise ValidationError("Min experience cannot be greater than max experience.")

    # ===== SAVE =====
    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.company.company_name
            if self.title:
                base += f"-{self.title.name}"
            super().save(*args, **kwargs)
            self.slug = slugify(f"{base}-{self.id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name} | {self.title}"
