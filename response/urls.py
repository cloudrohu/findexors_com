# response/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 📄 CRUD VIEWS
    path('', views.ResponseListView.as_view(), name='response_list'),
    path('<int:pk>/', views.ResponseDetailView.as_view(), name='response_detail'),
    path('<int:pk>/update/', views.ResponseUpdateView.as_view(), name='response_update'),
    path('<int:pk>/delete/', views.ResponseDeleteView.as_view(), name='response_delete'),

    # 📊 FILTERED STATUS VIEW
    path('status/<str:status>/', views.ResponseStatusView.as_view(), name='response_status'),

    # 📅 MEETINGS
    path('meetings/', views.MeetingListView.as_view(), name='response_meetings'),

    # ⚡ AJAX ENDPOINTS
    path('<int:pk>/ajax/update-status/', views.ajax_update_status, name='ajax_update_status'),
    path('<int:pk>/ajax/add-comment/', views.ajax_add_comment, name='ajax_add_comment'),
    path('<int:pk>/ajax/add-voice/', views.ajax_add_voice, name='ajax_add_voice'),
]
