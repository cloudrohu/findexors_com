from django import forms
from .models import Company, Comment, VoiceRecording, Visit,Meeting


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['company', 'comment']


class VoiceRecordingForm(forms.ModelForm):  # ✅ This must exist
    class Meta:
        model = VoiceRecording
        fields = ['company', 'file']


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['company', 'visit_for', 'visit_type', 'visit_status', 'comment']



class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status', 'meeting_date', 'assigned_to', 'comment']
        widgets = {
            'meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meeting comment'}),
        }
