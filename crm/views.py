import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, F
from django.http import HttpResponseRedirect
from django.views import View

# मान लीजिए कि Lead, FollowUp, ProductService आपके models.py में define हैं
# और LeadForm, FollowUpForm, AssignLeadForm आपके forms.py में define हैं।
# चूंकि models/forms code उपलब्ध नहीं है, हम केवल views structure पर focus कर रहे हैं।

# DUMMY CLASSES/MODELS/FORMS (असली data के लिए इन्हें बदलें)
# --- (production code में आपको ये imports models.py/forms.py से करने होंगे)
class Lead:
    # Dummy Model
    # 💡 FIX: FieldError से बचने के लिए minimal fields set कर रहे हैं।
    objects = None
    name = ''
    email = ''
    phone = ''
    status = 'New'
    source = 'Web'
    assigned_to = None
    notes = ''
    
    # DUMMY method for LeadDetailView context access
    def get_absolute_url(self):
        return '/'

class FollowUp:
    # Dummy Model
    objects = None
    pass
class ProductService:
    # Dummy Model
    objects = None
    pass
class LeadForm:
    # Dummy Form
    pass
class FollowUpForm:
    # Dummy Form
    pass
class AssignLeadForm:
    # Dummy Form
    pass
# ---

# LEAD MANAGEMENT VIEWS
class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leads'
    
    # Staff को केवल वे leads दिखाई देंगी जो उन्हें assigned हैं, या unassigned leads.
    def get_queryset(self):
        # वास्तविक logic यहाँ लागू करें
        return [] # 💡 FIX: Empty list return करें क्योंकि Dummy Model में objects नहीं हैं

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'
    
    # Dummy object return करें क्योंकि get_object_or_404 काम नहीं करेगा
    def get_object(self, queryset=None):
        return Lead()
    
    # Forms को detail view में pass करने के लिए get_context_data का उपयोग करें
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()
        
        # FollowUp Form और Assigned Form
        context['followup_form'] = FollowUpForm()
        # 💡 FIX: Lead object से assigned_to field access करने से बचने के लिए इसे comment करें 
        # context['assign_form'] = AssignLeadForm(initial={'assigned_to': lead.assigned_to})
        context['assign_form'] = AssignLeadForm() 
        
        # Lead के सभी follow-ups को Fetch करें
        # context['followups'] = FollowUp.objects.filter(lead=lead).order_by('-date_added')
        
        return context

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    # 💡 FIX: केवल minimal fields का उपयोग करें जो हमने DUMMY Lead class में set किए हैं
    fields = ['name', 'email', 'phone', 'status', 'source', 'assigned_to'] 
    template_name = 'crm/lead_create.html'
    success_url = reverse_lazy('lead_list')

# 💡 MISSING CLASS FIX: यह क्लास LeadUpdateView है जिसकी वजह से error आ रही थी।
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    # 💡 FIX: केवल minimal fields का उपयोग करें
    fields = ['name', 'email', 'phone', 'status', 'source', 'assigned_to', 'notes'] 
    template_name = 'crm/lead_update.html'
    
    # success_url को lead_detail page पर सेट करें
    def get_success_url(self):
        return reverse('lead_detail', kwargs={'pk': self.object.pk})

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('lead_list')

class AddFollowUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = FollowUpForm(request.POST)
        
        if form.is_valid():
            # FollowUp Logic यहाँ लागू करें
            # followup = form.save(commit=False)
            # followup.lead = lead
            # followup.staff_member = request.user
            # followup.save()
            return redirect('lead_detail', pk=pk)
            
        # Error होने पर Lead Detail Page पर redirect करें
        return redirect('lead_detail', pk=pk)
        
# -----------------------------------------------

# PRODUCT/SERVICE VIEWS (Placeholder)
class ProductServiceListView(LoginRequiredMixin, ListView):
    model = ProductService
    template_name = 'crm/product_list.html'
    context_object_name = 'products'
    
class ProductServiceCreateView(LoginRequiredMixin, CreateView):
    model = ProductService
    fields = ['name', 'price', 'description']
    template_name = 'crm/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductService
    fields = ['name', 'price', 'description']
    template_name = 'crm/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductService
    template_name = 'crm/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# -----------------------------------------------

# REPORTING VIEW (Updated in a previous step)
def report_view(request):
    # Dummy/Placeholder Aggregation logic
    # lead_status_report = Lead.objects.values('status').annotate(count=Count('status')).order_by('status')
    # staff_performance = Staff.objects.annotate(total_leads=Count('lead_set'))
    
    context = {
        'total_leads': 150, # Dummy Data
        'total_won_leads': 45, # Dummy Data
        'lead_status_report': [{'status': 'Won', 'count': 45}, {'status': 'New', 'count': 60}, {'status': 'Contacted', 'count': 45}],
        'staff_performance': [{'staff_member__username': 'admin', 'total_leads': 100}, {'staff_member__username': 'user1', 'total_leads': 50}],
    }
    return render(request, 'crm/report.html', context)
