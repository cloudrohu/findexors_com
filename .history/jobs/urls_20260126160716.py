# jobs/urls.py
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("create/", views.create_job, name="create"),
    path("ajax/load-localities/", views.ajax_load_localities, name="ajax_load_localities"),
]
