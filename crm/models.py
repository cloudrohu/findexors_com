# crm/models.py

from django.db import models
from django.contrib.auth.models import User

# 1. Staff Model
class Staff(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='response_staff'   # ✅ unique related name
    )
    # ot
# 2. Lead Model
class Lead(models.Model):
    STATUS_CHOICES = [
        ('New', 'नया'), ('Contacted', 'संपर्क किया गया'), 
        ('Qualified', 'योग्य'), ('Lost', 'खो गया'), ('Won', 'जीता गया'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    
    # Lead Assignment Feature
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 3. ProductService Model (उत्पाद/सेवा प्रबंधन)
class ProductService(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=[('Product', 'उत्पाद'), ('Service', 'सेवा')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# 4. FollowUp Model (कस्टमर फॉलो-अप और रिकॉर्डिंग)
class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='followups')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=[('Call', 'कॉल'), ('Email', 'ईमेल'), ('Meeting', 'मीटिंग')])
    notes = models.TextField()
    followup_date = models.DateTimeField()
    
    # Voice Recording Feature
    voice_recording = models.FileField(upload_to='call_recordings/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} for {self.lead.name}"

# 5. Sale Model (बिक्री प्रबंधन)
class Sale(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductService) 
    status = models.CharField(max_length=20, choices=[('Pending', 'लंबित'), ('Closed Won', 'डील जीता गया'), ('Closed Lost', 'डील खो गया')], default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    
    def __str__(self):
        return f"Sale for {self.lead.name}"