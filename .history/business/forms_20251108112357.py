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
        fields = '__all__'  # 👈 all editable fields visible
        exclude = ('created_by', 'updated_by', 'create_at', 'update_at')  # optional
        widgets = {
            'meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter meeting comment...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For consistent UI
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
