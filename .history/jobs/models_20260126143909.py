from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from utility.models import City, Locality


class Job(models.Model):

    # ================= CHOICES =================
    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("freelance", "Freelance"),
    ]

    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher"),
        ("0_1", "0-1 Year"),
        ("1_3", "1-3 Years"),
        ("3_5", "3-5 Years"),
        ("5_plus", "5+ Years"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("closed", "Closed"),
    ]

    # ================= BASIC INFO =================
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    company_name = models.CharField(max_length=255)

    # ================= JOB DETAILS =================
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default="full_time"
    )

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="fresher"
    )

    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)

    city = models.ForeignKey(
        City,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    locality = models.ForeignKey(
        Locality,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    # Display location (e.g. "Malad East, Mumbai")
    location = models.CharField(max_length=255, blank=True)

    openings = models.PositiveIntegerField(default=1)

    # ================= DESCRIPTION =================
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)

    # ================= META =================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="jobs_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="jobs_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ================= SAVE =================
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
