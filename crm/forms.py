# crm/forms.py

from django import forms
# 👇 यहाँ Lead को एक ही बार रखा गया है
from .models import FollowUp, Lead, Staff, Sale, ProductService 


# =================================================================
#                         1. FOLLOW-UP FORM
# =================================================================
class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        # Voice Recording Field को Form में जोड़ा गया
        fields = ['type', 'notes', 'followup_date', 'voice_recording'] 
        widgets = {
            # HTML5 datetime-local widget का उपयोग
            'followup_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            # voice_recording को Django अपने आप हैंडल करता है
        }

# =================================================================
#                         2. LEAD ASSIGNMENT/STATUS FORM
# =================================================================
class LeadAssignForm(forms.ModelForm):
    # सभी स्टाफ को चुनने के लिए फील्ड
    assigned_to = forms.ModelChoiceField(
        queryset=Staff.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 
    
    class Meta:
        model = Lead
        # status फील्ड पर भी फॉर्म-कंट्रोल क्लास जोड़ें
        fields = ['assigned_to', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


# =================================================================
#                         3. SALE CREATION FORM
# =================================================================
class SaleCreateForm(forms.ModelForm):
    # Sale मॉडल में M2M (ManyToManyField) होने के कारण, 'products' फील्ड को 
    # स्पष्ट रूप से निर्दिष्ट करना ज़रूरी है और इसे फॉर्म-कंट्रोल क्लास से अलग रखना होगा
    products = forms.ModelMultipleChoiceField(
        queryset=ProductService.objects.all(),
        # CheckboxSelectMultiple को कस्टम स्टाइलिंग की आवश्यकता होती है
        widget=forms.CheckboxSelectMultiple, 
        label="बेचे गए उत्पाद/सेवाएं",
        required=False
    )

    class Meta:
        model = Sale
        # lead को fields में शामिल नहीं किया जाता है, क्योंकि इसे view में जोड़ा जाएगा
        fields = ['status', 'amount', 'sale_date', 'products'] 
        
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }