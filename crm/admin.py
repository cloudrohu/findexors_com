# crm/admin.py

from django.contrib import admin
from .models import Lead, FollowUp, ProductService, Staff, Sale

# FollowUp को Lead डिटेल पेज पर दिखाने के लिए
class FollowUpInline(admin.TabularInline):
    model = FollowUp
    extra = 1

# Lead Model को Admin में दिखाना
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # Reporting: List display पर मुख्य फील्ड्स दिखती हैं
    list_display = ('name', 'status', 'assigned_to', 'created_at')
    # Reporting: इन फील्ड्स के द्वारा डेटा Filter किया जा सकता है
    list_filter = ('status', 'assigned_to')
    search_fields = ('name', 'email', 'phone')
    # Assignment: FollowUps को सीधे Lead पेज पर मैनेज किया जा सकता है
    inlines = [FollowUpInline] 

# बाकी मॉडल्स को रजिस्टर करें
admin.site.register(ProductService)
admin.site.register(Staff)
admin.site.register(Sale)