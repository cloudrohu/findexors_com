# jobs/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
        }
