from django import forms
from .models import Job

# Professional Tailwind Style Constant
TW_CLASS = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border"

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["slug", "created_by", "created_at", "updated_at", "status"]
        widgets = {
            "company": forms.Select(attrs={"class": TW_CLASS}),
            "title": forms.Select(attrs={"class": TW_CLASS}),
            "category": forms.Select(attrs={"class": TW_CLASS}),
            "industry": forms.Select(attrs={"class": TW_CLASS}),
            "openings": forms.NumberInput(attrs={"class": TW_CLASS}),
            "job_type": forms.Select(attrs={"class": TW_CLASS}),
            "work_location_type": forms.RadioSelect(attrs={"class": "hidden peer"}), # Custom radio style
            "city": forms.Select(attrs={"class": TW_CLASS}),
            "locality": forms.Select(attrs={"class": TW_CLASS}),
            "gender": forms.RadioSelect(attrs={"class": "hidden peer"}),
            "min_experience_months": forms.NumberInput(attrs={"class": TW_CLASS, "placeholder": "Min Months"}),
            "max_experience_months": forms.NumberInput(attrs={"class": TW_CLASS, "placeholder": "Max Months"}),
            "salary_type": forms.Select(attrs={"class": TW_CLASS}),
            "salary_min": forms.NumberInput(attrs={"class": TW_CLASS}),
            "salary_max": forms.NumberInput(attrs={"class": TW_CLASS}),
            "start_time": forms.TimeInput(attrs={"class": TW_CLASS, "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": TW_CLASS, "type": "time"}),
            "working_days": forms.Select(attrs={"class": TW_CLASS}),
            # Multiple selection for skills/tags
            "skills": forms.CheckboxSelectMultiple(),
            "benefits": forms.CheckboxSelectMultiple(),
            "languages": forms.CheckboxSelectMultiple(),
        }