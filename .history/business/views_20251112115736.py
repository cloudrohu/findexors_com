# views.py
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

# --- Models ---
from .models import (
    Company, Comment, VoiceRecording, Visit, Meeting, Followup
)
from response.models import Staff
from utility.models import (
    City, Locality, Sub_Locality, Category, Find_Form, Googlemap_Status, SocialSite
)

# --- Forms ---
from .forms import (
    CompanyForm, CommentForm, VoiceRecordingForm, VisitForm,
    MeetingForm, FollowupForm
)

# ============================================================
# Dependent dropdowns (City -> Locality -> SubLocality)
# ============================================================
def get_localities(request):
    city_id = request.GET.get("city_id")
    rows = Locality.objects.filter(city_id=city_id).values("id", "title")
    return JsonResponse(list(rows), safe=False)

def get_sub_localities(request):
    locality_id = request.GET.get("locality_id")
    rows = Sub_Locality.objects.filter(locality_id=locality_id).values("id", "title")
    return JsonResponse(list(rows), safe=False)

# ============================================================
# Inline formset factories
# ============================================================
MeetingFormSet   = inlineformset_factory(Company, Meeting,   form=MeetingForm,   extra=1, can_delete=True)
FollowupFormSet  = inlineformset_factory(Company, Followup,  form=FollowupForm,  extra=1, can_delete=True)
CommentFormSet   = inlineformset_factory(Company, Comment,   form=CommentForm,   extra=1, can_delete=True)
VoiceFormSet     = inlineformset_factory(Company, VoiceRecording, form=VoiceRecordingForm, extra=1, can_delete=True)
VisitFormSet     = inlineformset_factory(Company, Visit,     form=VisitForm,     extra=1, can_delete=True)

# ============================================================
# Helper mixin to save inline formsets (sets audit fields)
# ============================================================
class FormsetSaveMixin:
    """
    Call self.save_formsets(company) after saving the main form.
    Expects formset instances to be in context keys:
      meeting_formset, followup_formset, comment_formset, voice_formset, visit_formset
    """
    def build_formsets(self, instance=None):
        if self.request.POST:
            return {
                'meeting_formset':  MeetingFormSet(self.request.POST, self.request.FILES, instance=instance),
                'followup_formset': FollowupFormSet(self.request.POST, self.request.FILES, instance=instance),
                'comment_formset':  CommentFormSet(self.request.POST, self.request.FILES, instance=instance),
                'voice_formset':    VoiceFormSet(self.request.POST, self.request.FILES, instance=instance),
                'visit_formset':    VisitFormSet(self.request.POST, self.request.FILES, instance=instance),
            }
        else:
            return {
                'meeting_formset':  MeetingFormSet(instance=instance),
                'followup_formset': FollowupFormSet(instance=instance),
                'comment_formset':  CommentFormSet(instance=instance),
                'voice_formset':    VoiceFormSet(instance=instance),
                'visit_formset':    VisitFormSet(instance=instance),
            }

    def save_formsets(self, company):
        """
        Valid formsets are saved; audit fields filled.
        Returns (is_all_valid, errors_dict)
        """
        formsets = self.build_formsets(instance=company)
        all_valid = True
        errors = {}

        for key, fs in formsets.items():
            if not fs.is_valid():
                all_valid = False
                errors[key] = fs.errors

        if not all_valid:
            return False, errors

        # Save each formset, setting audit fields
        def set_audit(o):
            # created_by / updated_by
            if hasattr(o, 'created_by') and not getattr(o, 'created_by', None):
                o.created_by = self.request.user
            if hasattr(o, 'updated_by'):
                o.updated_by = self.request.user
            if hasattr(o, 'uploaded_by') and not getattr(o, 'uploaded_by', None):
                o.uploaded_by = self.request.user

        for fs in formsets.values():
            objs = fs.save(commit=False)
            for obj in objs:
                obj.company = company  # ensure FK set
                set_audit(obj)
                obj.save()
            fs.save_m2m()
            # handle deletions
            for obj in fs.deleted_objects:
                obj.delete()

        return True, {}

# ============================================================
# Company CRUD (only Create/Update shown here with inlines)
# ============================================================
class CompanyCreateView(LoginRequiredMixin, FormsetSaveMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'
    success_url = reverse_lazy('company_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.build_formsets())  # empty formsets for GET
        return ctx

    def form_valid(self, form):
        # set audit on main object
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)  # saves company
        ok, errors = self.save_formsets(self.object)
        if not ok:
            # if child invalid, re-render with errors
            context = self.get_context_data(form=form)
            context.update(self.build_formsets(instance=self.object))
            for k, v in errors.items():
                context[k] = context[k].__class__(self.request.POST, self.request.FILES, instance=self.object)
                context[k]._errors = v
            return self.render_to_response(context)
        return response


class CompanyUpdateView(LoginRequiredMixin, FormsetSaveMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.build_formsets(instance=self.object))
        return ctx

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        ok, errors = self.save_formsets(self.object)
        if not ok:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        return response

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

# ============================================================
# (Optional) List / Detail / Delete — keep your existing ones
# ============================================================

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'business/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        qs = Company.objects.select_related('city', 'locality', 'category').order_by('-create_at')
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        city = self.request.GET.get('city')
        locality = self.request.GET.get('locality')
        created_by = self.request.GET.get('created_by')
        if category: qs = qs.filter(category_id=category)
        if status: qs = qs.filter(status=status)
        if city: qs = qs.filter(city_id=city)
        if locality: qs = qs.filter(locality_id=locality)
        if created_by: qs = qs.filter(created_by_id=created_by)
        return qs

class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'business/company_detail.html'
    context_object_name = 'company'

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'business/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')
