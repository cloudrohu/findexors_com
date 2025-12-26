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

class Find_Form(models.Model):    
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name_plural='1. Find_Form'

class Googlemap_Status(models.Model):    
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name_plural='4. Googlemap_Status'

class Call_Status(models.Model):
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='2. Call_Status'

class SocialSite(models.Model):
    title = models.CharField(max_length=50,unique=True)   
    code = models.CharField(max_length=50,unique=True,null=True , blank=True)   
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='3. SocialSite'

class City(models.Model):
    title = models.CharField(max_length=500,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Locality(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(default="", blank=True)
    keywords = models.CharField(max_length=255, default="", blank=True)
    slug = models.SlugField(unique=True , null=True , blank=True)
    

    def __str__(self):
        return self.title
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Locality ,self).save(*args , **kwargs)
    
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('locality_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Meeting_Followup_Type(models.Model):
    title = models.CharField(max_length=100,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class RequirementType(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='4. Requirement_Type'

class Response_Status(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='5. Response_Status'


# ============================================================
# CATEGORY MODEL
# ============================================================
class Category(MPTTModel):

    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=50)

    icon = models.ImageField(
        upload_to='category/icons/',
        blank=True,
        null=True
    )


    slug = models.SlugField(unique=True, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        full_path = [self.title]
        parent = self.parent
        while parent:
            full_path.append(parent.title)
            parent = parent.parent
        return " / ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # ✅ URL (namespace-based)
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    # ✅ Admin preview
    def icon_tag(self):
        if self.icon:
            return mark_safe(
                f'<img src="{self.icon.url}" style="height:40px;width:40px;object-fit:contain;" />'
            )
        return "—"

    icon_tag.short_description = "Icon"

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "utility_category"   # 🔥 THIS FIXES EVERYTHING

# ============================================================
# Sub_Locality MODEL
# ============================================================
class Sub_Locality(models.Model):
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title   

    class Meta:
        verbose_name_plural = "Sub Locality"

    def get_absolute_url(self):
        return reverse('sub_locality_detail', kwargs={'slug': self.slug})


