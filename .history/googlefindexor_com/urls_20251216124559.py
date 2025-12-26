from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as IndexView # केवल home के views को यहाँ इम्पोर्ट करें

urlpatterns = [
    # ------------------------------------
    # 1. DJANGO ADMIN / AUTH URLs
    # ------------------------------------
    path('accounts/', include('django.contrib.auth.urls')), 
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    
    # ------------------------------------
    # 2. HOME App URLs (Main/Root Pages)
    # ------------------------------------
    path('', include('home.urls')), # Home app manages the root path ('/')

    
   
    # ------------------------------------
    # 4. RESPONSE App URLs (All paths start with 'response/')
    # ------------------------------------
    path('response/', include('response.urls')), # Dashboard, Response CRUD
    path('business/', include('business.urls')), # Dashboard, Response CRUD

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
