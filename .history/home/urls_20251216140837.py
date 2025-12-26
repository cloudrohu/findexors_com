from django.urls import path

from home.views import IndexView,DashboardView,company_meeting_list, response_meeting_list
from .import views 

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('ajax/search/', views.ajax_search_suggestions, name='ajax_search'),
    path("admin/logout/", LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    # 🏢 Company Meetings Filter Views
    path('company-meetings/<str:filter_type>/', company_meeting_list, name='company_meeting_list'),

    # 📊 Response Meetings Filter Views
    path('response-meetings/<str:filter_type>/', response_meeting_list, name='response_meeting_list'),

    path('company-meetings/edit/<int:pk>/', views.edit_company_meeting, name='edit_company_meeting'),
    path('response-meetings/edit/<int:pk>/', views.edit_response_meeting, name='edit_response_meeting'),

    path('ajax/get-localities/', views.get_localities, name='get_localities'),
    path('ajax/get-sub-localities/', views.get_sub_localities, name='get_sub_localities'),
    
]
