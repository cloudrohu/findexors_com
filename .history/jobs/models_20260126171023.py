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
    # Choices
    JOB_TYPE_CHOICES = [("full_time", "Full Time"), ("part_time", "Part Time"), ("contract", "Contract")]
    WORK_LOCATION_CHOICES = [("office", "Office"), ("field", "Field"), ("home", "WFH")]
    GENDER_CHOICES = [("any", "Any"), ("male", "Male"), ("female", "Female")]
    SALARY_TYPE_CHOICES = [("fixed", "Fixed"), ("fixed_incentive", "Fixed + Incentive"), ("commission", "Commission")]
    STATUS_CHOICES = [("draft", "Draft"), ("active", "Active"), ("closed", "Closed")]

    # Basic Info
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    openings = models.PositiveIntegerField(default=1)

    # Location & Type
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_location_type = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default="office")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    # Salary & Time
    salary_type = models.CharField(max_length=30, choices=SALARY_TYPE_CHOICES, default="fixed")
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    working_days = models.ForeignKey(WorkingDaysOption, on_delete=models.SET_NULL, null=True, blank=True)

    # Candidate Preferences
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    min_experience_months = models.PositiveIntegerField(default=0)
    max_experience_months = models.PositiveIntegerField(default=0)

    # Tags & Requirements (Fixes Admin Errors)
    skills = models.ManyToManyField(JobSkill, blank=True)
    benefits = models.ManyToManyField(JobBenefit, blank=True)
    assets = models.ManyToManyField(JobAsset, blank=True) # Added back
    documents = models.ManyToManyField(JobDocument, blank=True) # Added back
    languages = models.ManyToManyField(JobLanguageRequirement, blank=True)

    # Description
    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)

    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.company.company_name}-{self.title}-{self.id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"from django.db import models
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
    # Choices
    JOB_TYPE_CHOICES = [("full_time", "Full Time"), ("part_time", "Part Time"), ("contract", "Contract")]
    WORK_LOCATION_CHOICES = [("office", "Office"), ("field", "Field"), ("home", "WFH")]
    GENDER_CHOICES = [("any", "Any"), ("male", "Male"), ("female", "Female")]
    SALARY_TYPE_CHOICES = [("fixed", "Fixed"), ("fixed_incentive", "Fixed + Incentive"), ("commission", "Commission")]
    STATUS_CHOICES = [("draft", "Draft"), ("active", "Active"), ("closed", "Closed")]

    # Basic Info
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    openings = models.PositiveIntegerField(default=1)

    # Location & Type
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_location_type = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default="office")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    # Salary & Time
    salary_type = models.CharField(max_length=30, choices=SALARY_TYPE_CHOICES, default="fixed")
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    working_days = models.ForeignKey(WorkingDaysOption, on_delete=models.SET_NULL, null=True, blank=True)

    # Candidate Preferences
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    min_experience_months = models.PositiveIntegerField(default=0)
    max_experience_months = models.PositiveIntegerField(default=0)

    # Tags & Requirements (Fixes Admin Errors)
    skills = models.ManyToManyField(JobSkill, blank=True)
    benefits = models.ManyToManyField(JobBenefit, blank=True)
    assets = models.ManyToManyField(JobAsset, blank=True) # Added back
    documents = models.ManyToManyField(JobDocument, blank=True) # Added back
    languages = models.ManyToManyField(JobLanguageRequirement, blank=True)

    # Description
    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)

    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.company.company_name}-{self.title}-{self.id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"