from django import forms
from .models import Job

TAILWIND_INPUT = {
    "class": "mt-2 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
}

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["slug", "created_by", "created_at", "updated_at"]
        widgets = {
            "company": forms.Select(attrs=TAILWIND_INPUT),
            "title": forms.Select(attrs=TAILWIND_INPUT),
            "category": forms.Select(attrs=TAILWIND_INPUT),
            "openings": forms.NumberInput(attrs=TAILWIND_INPUT),
            "job_type": forms.Select(attrs=TAILWIND_INPUT),
            "work_location_type": forms.RadioSelect(),
            "city": forms.Select(attrs=TAILWIND_INPUT),
            "locality": forms.Select(attrs=TAILWIND_INPUT),
            "gender": forms.RadioSelect(),
            "min_experience_months": forms.NumberInput(attrs=TAILWIND_INPUT),
            "max_experience_months": forms.NumberInput(attrs=TAILWIND_INPUT),
            "salary_type": forms.Select(attrs=TAILWIND_INPUT),
            "salary_min": forms.NumberInput(attrs=TAILWIND_INPUT),
            "salary_max": forms.NumberInput(attrs=TAILWIND_INPUT),
            "start_time": forms.TimeInput(attrs={**TAILWIND_INPUT, "type": "time"}),
            "end_time": forms.TimeInput(attrs={**TAILWIND_INPUT, "type": "time"}),
            "working_days": forms.Select(attrs=TAILWIND_INPUT),
            "description": forms.Textarea(attrs={
                **TAILWIND_INPUT, "rows": 5
            }),
            "requirements": forms.Textarea(attrs={
                **TAILWIND_INPUT, "rows": 4
            }),
        }
