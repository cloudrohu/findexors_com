from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.text import slugify

from utility.models import Find_Form, Call_Status,SocialSite,Googlemap_Status,City,Locality

# Create your models here.



class Company(models.Model):    
    company_response = models.CharField(max_length=50,unique=False)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(max_length=255,null=True , blank=True)
    googleads_account_date=models.DateTimeField(auto_now=True)

    company = models.CharField(max_length=255,null=True , blank=True)
    contact_no = models.CharField(max_length=255,null=True , blank=True)
    address = models.CharField(max_length=500,null=True , blank=True)
    keywords = models.CharField(max_length=255,null=True , blank=True)
    website = models.CharField(max_length=255,null=True , blank=True)
    google_map = models.CharField(max_length=1000,null=True , blank=True)
    description = models.CharField(max_length=1000,null=True , blank=True)
   
    slug = models.SlugField(max_length=500,null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

    def __str__(self):
        return self.email
    