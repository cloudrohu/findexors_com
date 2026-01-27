from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = [
            "slug",
            "created_by",
            "created_at",
            "updated_at",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
