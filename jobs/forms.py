# jobs/forms.py
from django import forms
from .models import Job

TW = "mt-1 block w-full rounded-lg border border-gray-300 p-2.5 focus:ring-indigo-500 focus:border-indigo-500"

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["slug", "status", "created_by", "updated_by", "created_at", "updated_at"]

        widgets = {
            "company": forms.Select(attrs={"class": TW}),
            "title": forms.Select(attrs={"class": TW}),
            "category": forms.Select(attrs={"class": TW}),
            "industry": forms.Select(attrs={"class": TW}),
            "openings": forms.NumberInput(attrs={"class": TW}),
            "job_type": forms.Select(attrs={"class": TW}),
            "work_location_type": forms.RadioSelect(),
            "city": forms.Select(attrs={"class": TW}),
            "locality": forms.Select(attrs={"class": TW}),
            "gender": forms.RadioSelect(),
            "min_experience_months": forms.NumberInput(attrs={"class": TW}),
            "max_experience_months": forms.NumberInput(attrs={"class": TW}),
            "salary_type": forms.Select(attrs={"class": TW}),
            "salary_min": forms.NumberInput(attrs={"class": TW}),
            "salary_max": forms.NumberInput(attrs={"class": TW}),
            "start_time": forms.TimeInput(attrs={"class": TW, "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": TW, "type": "time"}),
            "working_days": forms.Select(attrs={"class": TW}),
            "skills": forms.CheckboxSelectMultiple(),
            "benefits": forms.CheckboxSelectMultiple(),
            "languages": forms.CheckboxSelectMultiple(),
        }
