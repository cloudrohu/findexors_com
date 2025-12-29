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

    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

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

class Sub_Locality((models.Model)):
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

class PropertyType(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Parent Type/Category'
    )
    
    is_top_level = models.BooleanField(default=False) 
    
    is_selectable = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "Property Types"

    def __str__(self):
        full_path = [node.name for node in self.get_ancestors(include_self=True)]
        return ' / '.join(full_path)
    
class PossessionIn(models.Model):
    year = models.PositiveIntegerField(
        unique=True,
        help_text="e.g. 2025"
    )

    class Meta:
        verbose_name = "Possession Year"
        verbose_name_plural = "Possession Years"
        ordering = ['year']

    def __str__(self):
        return str(self.year)

class ProjectAmenities(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='amenities/', blank=True, null=True)
    
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title

class Bank(models.Model):
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='03. Bank'

class PropertyAmenities(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='property/amenities/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Property Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

    def icon_tag(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="40" height="40" />')
        return ""
    icon_tag.short_description = "Icon"

