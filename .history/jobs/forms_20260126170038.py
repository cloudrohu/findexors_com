# jobs/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = [
            "slug",
            "status",        # ✅ STATUS HIDDEN (no error)
            "created_by",
            "created_at",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
        }
