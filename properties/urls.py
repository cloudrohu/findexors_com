from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='properties'),

    path('residential/',views.residential_projects,name='residential_projects'),

    path('commercial/',views.commercial_projects,name='commercial_projects'),

    path('search/',views.search_projects,name='search_projects'),

    path('submit-enquiry/<int:id>/',views.submit_enquiry,name='submit_enquiry'),

    path('thank-you/',views.thank_you,name='thank_you'),

    path('api/search-suggestions/',views.search_suggestions,name='search_suggestions'),


    path(
        'api/search-suggestions/',
        views.search_suggestions,
        name='search_suggestions'
    ),

    path(
        'search/',
        views.search_projects,
        name='search_projects'
    ),

    path('search/',views.search_projects,name='search_projects'),

    # Project Details
    path('<int:id>/<slug:slug>/',views.project_details,name='project_details'),
]