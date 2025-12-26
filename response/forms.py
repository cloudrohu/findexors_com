from django import forms
from .models import Response, Meeting, Followup, Comment, VoiceRecording


# =======================
#  Response Form
# =======================
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'status', 'contact_no', 'assigned_to', 'contact_persone',
            'business_name', 'business_category', 'requirement_types',
            'city', 'locality'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'contact_persone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'business_category': forms.Select(attrs={'class': 'form-select'}),
            'requirement_types': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'locality': forms.Select(attrs={'class': 'form-select'}),
        }


# =======================
#  Meeting Form
# =======================
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'response', 'status', 'meeting_date', 'assigned_to', 'comment'
        ]
        widgets = {
            'response': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'meeting_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# =======================
#  Followup Form
# =======================
class FollowupForm(forms.ModelForm):
    class Meta:
        model = Followup
        fields = [
            'response', 'status', 'followup_date', 'assigned_to', 'comment'
        ]
        widgets = {
            'response': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'followup_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# =======================
#  Comment Form
# =======================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['response', 'comment']
        widgets = {
            'response': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your comment...'}),
        }


# =======================
#  Voice Recording Form
# =======================
class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['response', 'file', 'note']
        widgets = {
            'response': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional note'}),
        }
