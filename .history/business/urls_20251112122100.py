# business/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),

    path('status/<str:status>/', views.CompanyStatusListView.as_view(), name='company_status'),

    path('<int:pk>/<slug:slug>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),

    # AJAX — company-scoped endpoints
    path('<int:pk>/ajax/add-comment/', views.ajax_add_comment, name='company_ajax_add_comment'),
    path('<int:pk>/ajax/add-voice/', views.ajax_add_voice, name='company_ajax_add_voice'),
    path('<int:pk>/ajax/update-status/', views.ajax_update_status, name='company_ajax_update_status'),
    path('<int:pk>/ajax/add-visit/', views.ajax_add_visit, name='company_ajax_add_visit'),

    # Company meetings list inside business
    path('company/meetings/', views.CompanyMeetingListView.as_view(), name='company_meetings'),
]
