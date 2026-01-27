from django import forms
from .models import Job


class JobCreateForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            "company",
            "title",
            "category",
            "industry",
            "openings",

            "job_type",
            "work_location_type",

            "city",
            "locality",

            "gender",
            "only_fresher",
            "min_experience_months",
            "max_experience_months",

            "salary_type",
            "salary_min",
            "salary_max",

            "start_time",
            "end_time",
            "working_days",

            "skills",
            "benefits",
            "assets",
            "documents",
            "languages",

            "description",
            "requirements",
        ]

        widgets = {
            "skills": forms.CheckboxSelectMultiple,
            "benefits": forms.CheckboxSelectMultiple,
            "assets": forms.CheckboxSelectMultiple,
            "documents": forms.CheckboxSelectMultiple,
            "languages": forms.CheckboxSelectMultiple,

            "description": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
        }
