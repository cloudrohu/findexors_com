from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_job, name="create_job"),
    path("ajax/load-localities/", views.ajax_load_localities, name="ajax_load_localities"),
]
