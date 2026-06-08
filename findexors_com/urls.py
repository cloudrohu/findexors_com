from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as IndexView # केवल home के views को यहाँ इम्पोर्ट करें

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')), 
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('home.urls')), # Home app manages the root path ('/')
    path("jobs/", include("jobs.urls")),
    path('business/', include('business.urls')),
    path('properties/', include('properties.urls')),
    path('furniture/', include('furniture.urls')),
    path('response/', include('response.urls')), # Dashboard, Response CRUD

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
