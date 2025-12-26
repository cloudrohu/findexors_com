import datetime
from django.urls import path
from . import views as crm_views # Import views from the local app

urlpatterns = [
    # ------------------
    # LEAD MANAGEMENT URLs
    # ------------------
    # List: /crm/ (or /leads/)
    path('', crm_views.LeadListView.as_view(), name='lead_list'), 
    
    # Detail: /crm/1/
    path('<int:pk>/', crm_views.LeadDetailView.as_view(), name='lead_detail'), 
    
    # Create: /crm/add/
    path('add/', crm_views.LeadCreateView.as_view(), name='lead_create'), 
    
    # Update: /crm/1/update/
    path('<int:pk>/update/', crm_views.LeadUpdateView.as_view(), name='lead_update'),
    
    # Delete: /crm/1/delete/
    path('<int:pk>/delete/', crm_views.LeadDeleteView.as_view(), name='lead_delete'), 
    
    # Follow-Up: /crm/1/followup/add/
    path('<int:pk>/followup/add/', crm_views.AddFollowUpView.as_view(), name='add_followup'),
    
    # ------------------
    # PRODUCT/SERVICE MANAGEMENT URLs
    # ------------------
    # List: /crm/products/
    path('products/', crm_views.ProductServiceListView.as_view(), name='product_list'), 
    
    # Create: /crm/products/add/
    path('products/add/', crm_views.ProductServiceCreateView.as_view(), name='product_create'),
    
    # Update: /crm/products/1/update/
    path('products/<int:pk>/update/', crm_views.ProductServiceUpdateView.as_view(), name='product_update'),
    
    # Delete: /crm/products/1/delete/
    path('products/<int:pk>/delete/', crm_views.ProductServiceDeleteView.as_view(), name='product_delete'),
    
    # ------------------
    # REPORTING URLS
    # ------------------
    # Report Page: /crm/report/
    path('report/', crm_views.report_view, name='report'), 
    
]
