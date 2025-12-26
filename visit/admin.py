import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *



class Follow_UpInline(admin.TabularInline):
    model = Follow_Up
    extra = 1
    show_change_link = True

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class Today_VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_thumbnail', 'company',  'status', 'description', 'followup_meeting','locality_city','create_at','update_at']    
    
    list_filter = ['create_at','locality_city','status','followup_meeting']
    search_fields = ['company','description']
    list_editable = ['followup_meeting','locality_city','status','description']
    list_per_page = 20
    inlines = [Follow_UpInline,MeetingInline]

@admin_thumbnails.thumbnail('image')
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meeting','comment', 'company','create_at','update_at']    
    
    list_filter = ('meeting','create_at','update_at',) 
    list_per_page = 30 


@admin_thumbnails.thumbnail('image')
class Follow_UpAdmin(admin.ModelAdmin):
    list_display = ['id',  'follow_up','comment','company', 'create_at','update_at']    
    
    list_filter = ('follow_up','create_at','update_at',) 
    list_per_page = 30 




admin.site.register(Follow_Up,Follow_UpAdmin)
admin.site.register(Meeting,MeetingAdmin)
admin.site.register(Today_Visit,Today_VisitAdmin)
admin.site.register(Visit_Type)








