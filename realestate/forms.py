from django import forms
from .models import Company, Comment, VoiceRecording, Visit, Meeting


# ============================================================
# 🏢 COMPANY FORM (FULLY EDITABLE)
# ============================================================
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at', 'slug')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Company address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website link'}),
            'google_map': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google map link'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'locality': forms.Select(attrs={'class': 'form-select'}),
            'sub_locality': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'followup_meeting': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'find_form': forms.Select(attrs={'class': 'form-select'}),
            'googlemap_status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


# ============================================================
# 💬 COMMENT FORM
# ============================================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['company', 'comment']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your comment...'}),
        }


# ============================================================
# 🎙️ VOICE RECORDING FORM
# ============================================================
class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['company', 'file']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ============================================================
# 🚶 VISIT FORM
# ============================================================
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['company', 'visit_for', 'visit_type', 'visit_status', 'comment']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'visit_for': forms.TextInput(attrs={'class': 'form-control'}),
            'visit_type': forms.Select(attrs={'class': 'form-select'}),
            'visit_status': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ============================================================
# 📅 MEETING FORM
# ============================================================
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at', 'company')  # 👈 Exclude company
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter meeting comment...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
