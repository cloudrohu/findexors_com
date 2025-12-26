# your_app/forms.py
from django import forms
from django.forms import ModelForm
from .models import (
    Company, Comment, VoiceRecording, Visit, Meeting, Followup,
    Approx, SocialLink, Error, Images, Faq
)
from response.models import Staff

# ------------------------------------------------------------
# Helpers: common widget classes
# ------------------------------------------------------------
TEXT_INPUT = {'class': 'form-control'}
SELECT = {'class': 'form-select'}
TEXTAREA = {'class': 'form-control', 'rows': 3}

# ------------------------------------------------------------
# Company Form
# ------------------------------------------------------------
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        # Exclude audit fields and slug (auto-generated)
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at', 'slug')
        widgets = {
            'company_name': forms.TextInput(attrs={**TEXT_INPUT, 'placeholder': 'Enter company name'}),
            'category': forms.Select(attrs=SELECT),
            'find_form': forms.Select(attrs=SELECT),
            'googlemap_status': forms.Select(attrs=SELECT),
            'city': forms.Select(attrs=SELECT),
            'locality': forms.Select(attrs=SELECT),
            'sub_locality': forms.Select(attrs=SELECT),
            'address': forms.Textarea(attrs={**TEXTAREA, 'rows': 2}),
            'contact_person': forms.TextInput(attrs=TEXT_INPUT),
            'contact_no': forms.TextInput(attrs={**TEXT_INPUT, 'placeholder': 'Mobile / Phone'}),
            'website': forms.TextInput(attrs=TEXT_INPUT),
            'google_map': forms.TextInput(attrs=TEXT_INPUT),
            'description': forms.Textarea(attrs={**TEXTAREA, 'rows': 2}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs=SELECT),
            'status': forms.Select(attrs=SELECT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add bootstrap class to any missing widgets
        for name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'


# ------------------------------------------------------------
# Comment Form
# (inline will be created with inlineformset_factory)
# ------------------------------------------------------------
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('company', 'comment')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'comment': forms.Textarea(attrs={**TEXTAREA, 'placeholder': 'Enter comment...'}),
        }


# ------------------------------------------------------------
# Voice Recording Form
# (file upload) - careful with cloning file inputs in JS
# ------------------------------------------------------------
class VoiceRecordingForm(ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ('company', 'file')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ------------------------------------------------------------
# Visit Form
# ------------------------------------------------------------
class VisitForm(ModelForm):
    class Meta:
        model = Visit
        # company is provided by inline/instance; keep for standalone if needed
        fields = ('company', 'visit_for', 'visit_type', 'visit_status', 'comment')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'visit_for': forms.Select(attrs=SELECT),
            'visit_type': forms.Select(attrs=SELECT),
            'visit_status': forms.Select(attrs=SELECT),
            'comment': forms.Textarea(attrs={**TEXTAREA, 'rows': 2}),
        }


# ------------------------------------------------------------
# Meeting Form
# ------------------------------------------------------------
class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        # exclude audit + company (company will be set by inline/instance)
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at', 'company')
        widgets = {
            'status': forms.Select(attrs=SELECT),
            # datetime-local works with HTML5; note: timezone handling on server
            'meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local', **TEXT_INPUT}),
            'assigned_to': forms.Select(attrs=SELECT),
            'comment': forms.Textarea(attrs={**TEXTAREA, 'rows': 2}),
        }


# ------------------------------------------------------------
# Followup Form
# ------------------------------------------------------------
class FollowupForm(ModelForm):
    class Meta:
        model = Followup
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at', 'company')
        widgets = {
            'status': forms.Select(attrs=SELECT),
            'followup_date': forms.DateTimeInput(attrs={'type': 'datetime-local', **TEXT_INPUT}),
            'assigned_to': forms.Select(attrs=SELECT),
            'comment': forms.Textarea(attrs={**TEXTAREA, 'rows': 2}),
        }


# ------------------------------------------------------------
# Approx Form (minor)
# ------------------------------------------------------------
class ApproxForm(ModelForm):
    class Meta:
        model = Approx
        fields = ('category', 'city', 'locality', 'title')
        widgets = {
            'category': forms.Select(attrs=SELECT),
            'city': forms.Select(attrs=SELECT),
            'locality': forms.Select(attrs=SELECT),
            'title': forms.TextInput(attrs={**TEXT_INPUT, 'placeholder': 'Title'}),
        }


# ------------------------------------------------------------
# SocialLink Form
# ------------------------------------------------------------
class SocialLinkForm(ModelForm):
    class Meta:
        model = SocialLink
        fields = ('company', 'socia_site', 'link')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'socia_site': forms.Select(attrs=SELECT),
            'link': forms.TextInput(attrs={**TEXT_INPUT, 'placeholder': 'https://...'}),
        }


# ------------------------------------------------------------
# Error Form
# ------------------------------------------------------------
class ErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ('company', 'title', 'error')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'title': forms.TextInput(attrs=TEXT_INPUT),
            'error': forms.TextInput(attrs=TEXT_INPUT),
        }


# ------------------------------------------------------------
# Images Form
# ------------------------------------------------------------
class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ('product', 'title', 'image')
        widgets = {
            'product': forms.Select(attrs=SELECT),
            'title': forms.TextInput(attrs=TEXT_INPUT),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ------------------------------------------------------------
# FAQ Form
# ------------------------------------------------------------
class FaqForm(ModelForm):
    class Meta:
        model = Faq
        fields = ('company', 'questions', 'answers')
        widgets = {
            'company': forms.Select(attrs=SELECT),
            'questions': forms.TextInput(attrs=TEXT_INPUT),
            'answers': forms.Textarea(attrs={**TEXTAREA, 'rows': 3}),
        }


# ------------------------------------------------------------
# Generic __init__ behavior (optional): ensure classes
# ------------------------------------------------------------
# If you want to apply the same 'form-control' to all forms automatically,
# uncomment the following mixin approach or call similar loop in each form __init__.
#
# (Already handled per-form above.)
