from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.core.files import File
import os
from datetime import datetime


from django.forms import inlineformset_factory
from django.shortcuts import redirect

from .forms import MeetingForm
from django.utils.timezone import now

from django.http import JsonResponse
from utility.models import Locality, Sub_Locality

def get_localities(request):
    city_id = request.GET.get("city_id")
    localities = Locality.objects.filter(city_id=city_id).values("id", "title")
    return JsonResponse(list(localities), safe=False)

def get_sub_localities(request):
    locality_id = request.GET.get("locality_id")
    sub_localities = Sub_Locality.objects.filter(locality_id=locality_id).values("id", "title")
    return JsonResponse(list(sub_localities), safe=False)



# 🎯 Import models and forms
from .models import Company, Comment, VoiceRecording, Visit, Meeting
from response.models import Staff

from .forms import CompanyForm, CommentForm, VoiceRecordingForm, VisitForm
from utility.models import (
    Find_Form, Call_Status, SocialSite,
    Googlemap_Status, City, Locality, Category
)

# =====================================================
# 📄 COMPANY LIST VIEW (with Filters)
# =====================================================
class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'business/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        qs = Company.objects.select_related('city', 'locality', 'category').order_by('-create_at')

        # 🔍 Filters
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        city = self.request.GET.get('city')
        locality = self.request.GET.get('locality')
        created_by = self.request.GET.get('created_by')
        followup_from = self.request.GET.get('followup_from')
        followup_to = self.request.GET.get('followup_to')

        if category:
            qs = qs.filter(category_id=category)
        if status:
            qs = qs.filter(status=status)
        if city:
            qs = qs.filter(city_id=city)
        if locality:
            qs = qs.filter(locality_id=locality)
        if created_by:
            qs = qs.filter(created_by_id=created_by)
        if followup_from:
            qs = qs.filter(followup_meeting__date__gte=parse_date(followup_from))
        if followup_to:
            qs = qs.filter(followup_meeting__date__lte=parse_date(followup_to))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🧩 City/Locality sorted alphabetically (fix for missing dropdown items)
        context['categories'] = Category.objects.all().order_by('title')
        context['cities'] = City.objects.all().order_by('title')
        context['localities'] = Locality.objects.all().order_by('title')
        context['users'] = User.objects.all().order_by('username')

        # Preserve filters during pagination
        context['querystring'] = "&".join(
            [f"{k}={v}" for k, v in self.request.GET.items() if k != 'page']
        )

        return context


# =====================================================
# 📄 COMPANY STATUS FILTER VIEW (optional: /status/<status>/)
# =====================================================
class CompanyStatusListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'business/company_list.html'
    context_object_name = 'companies'
    paginate_by = 5

    def get_queryset(self):
        status = self.kwargs.get('status')
        return (
            Company.objects.filter(status=status)
            .select_related('city', 'locality', 'category')
            .order_by('-create_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.kwargs.get('status')
        return context


# =====================================================
# 📝 COMPANY DETAIL VIEW
# =====================================================
class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'business/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['comments'] = Comment.objects.filter(company=company).order_by('-create_at')
        context['voice_recordings'] = VoiceRecording.objects.filter(company=company).order_by('-uploaded_at')
        context['visits'] = Visit.objects.filter(company=company).order_by('-uploaded_at')
        context['comment_form'] = CommentForm()
        context['voice_form'] = VoiceRecordingForm()
        context['visit_form'] = VisitForm()
        return context




# Inline formset factories
MeetingFormSet = inlineformset_factory(Company, Meeting, form=MeetingForm, extra=1, can_delete=True)
FollowupFormSet = inlineformset_factory(Company, Followup, extra=1, can_delete=True)
CommentFormSet = inlineformset_factory(Company, Comment, form=CommentForm, extra=1, can_delete=True)
VoiceFormSet = inlineformset_factory(Company, VoiceRecording, form=VoiceRecordingForm, extra=1, can_delete=True)
VisitFormSet = inlineformset_factory(Company, Visit, form=VisitForm, extra=1, can_delete=True)

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'
    success_url = reverse_lazy('company_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['meeting_formset'] = MeetingFormSet(self.request.POST, self.request.FILES)
            context['followup_formset'] = FollowupFormSet(self.request.POST, self.request.FILES)
            context['comment_formset'] = CommentFormSet(self.request.POST, self.request.FILES)
            context['voice_formset'] = VoiceFormSet(self.request.POST, self.request.FILES)
            context['visit_formset'] = VisitFormSet(self.request.POST, self.request.FILES)
        else:
            context['meeting_formset'] = MeetingFormSet()
            context['followup_formset'] = FollowupFormSet()
            context['comment_formset'] = CommentFormSet()
            context['voice_formset'] = VoiceFormSet()
            context['visit_formset'] = VisitFormSet()
        return context

    def form_valid(self, form):
        # save company first then formsets
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        company = self.object

        meeting_fs = MeetingFormSet(self.request.POST, self.request.FILES, instance=company)
        followup_fs = FollowupFormSet(self.request.POST, self.request.FILES, instance=company)
        comment_fs = CommentFormSet(self.request.POST, self.request.FILES, instance=company)
        voice_fs = VoiceFormSet(self.request.POST, self.request.FILES, instance=company)
        visit_fs = VisitFormSet(self.request.POST, self.request.FILES, instance=company)

        if meeting_fs.is_valid():
            ms = meeting_fs.save(commit=False)
            for m in ms:
                if hasattr(m, 'uploaded_by') and not m.uploaded_by:
                    m.uploaded_by = self.request.user
                if hasattr(m, 'created_by') and not m.created_by:
                    m.created_by = self.request.user
                m.save()
            meeting_fs.save_m2m()

        if followup_fs.is_valid():
            fs = followup_fs.save(commit=False)
            for f in fs:
                if hasattr(f, 'created_by') and not f.created_by:
                    f.created_by = self.request.user
                if hasattr(f, 'updated_by'):
                    f.updated_by = self.request.user
                f.save()
            followup_fs.save_m2m()

        if comment_fs.is_valid():
            cs = comment_fs.save(commit=False)
            for c in cs:
                if hasattr(c, 'created_by') and not c.created_by:
                    c.created_by = self.request.user
                if hasattr(c, 'updated_by'):
                    c.updated_by = self.request.user
                c.save()
            comment_fs.save_m2m()

        if voice_fs.is_valid():
            vs = voice_fs.save(commit=False)
            for v in vs:
                if hasattr(v, 'uploaded_by') and not v.uploaded_by:
                    v.uploaded_by = self.request.user
                v.save()
            voice_fs.save_m2m()

        if visit_fs.is_valid():
            vs2 = visit_fs.save(commit=False)
            for v in vs2:
                if hasattr(v, 'uploaded_by') and not v.uploaded_by:
                    v.uploaded_by = self.request.user
                v.company = company
                v.save()
            visit_fs.save_m2m()

        return response


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        if self.request.POST:
            context['meeting_formset'] = MeetingFormSet(self.request.POST, self.request.FILES, instance=company)
            context['followup_formset'] = FollowupFormSet(self.request.POST, self.request.FILES, instance=company)
            context['comment_formset'] = CommentFormSet(self.request.POST, self.request.FILES, instance=company)
            context['voice_formset'] = VoiceFormSet(self.request.POST, self.request.FILES, instance=company)
            context['visit_formset'] = VisitFormSet(self.request.POST, self.request.FILES, instance=company)
        else:
            context['meeting_formset'] = MeetingFormSet(instance=company)
            context['followup_formset'] = FollowupFormSet(instance=company)
            context['comment_formset'] = CommentFormSet(instance=company)
            context['voice_formset'] = VoiceFormSet(instance=company)
            context['visit_formset'] = VisitFormSet(instance=company)
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        company = self.object

        meeting_fs = MeetingFormSet(self.request.POST, self.request.FILES, instance=company)
        followup_fs = FollowupFormSet(self.request.POST, self.request.FILES, instance=company)
        comment_fs = CommentFormSet(self.request.POST, self.request.FILES, instance=company)
        voice_fs = VoiceFormSet(self.request.POST, self.request.FILES, instance=company)
        visit_fs = VisitFormSet(self.request.POST, self.request.FILES, instance=company)

        # same saving logic as in CreateView
        for fs in (meeting_fs, followup_fs, comment_fs, voice_fs, visit_fs):
            if fs.is_valid():
                instances = fs.save(commit=False)
                for inst in instances:
                    # set uploaded_by/created_by/updated_by if present
                    if hasattr(inst, 'uploaded_by') and not getattr(inst, 'uploaded_by', None):
                        inst.uploaded_by = self.request.user
                    if hasattr(inst, 'created_by') and not getattr(inst, 'created_by', None):
                        inst.created_by = self.request.user
                    if hasattr(inst, 'updated_by'):
                        inst.updated_by = self.request.user
                    inst.save()
                fs.save_m2m()

        return response

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})



# =====================================================
# 🗑 COMPANY DELETE VIEW
# =====================================================
class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'business/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')


# =====================================================
# 💬 AJAX: Add Comment
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_comment(request, pk):
    company = get_object_or_404(Company, pk=pk)
    comment_text = request.POST.get('comment')
    if comment_text and comment_text.strip():
        comment = Comment.objects.create(
            company=company,
            comment=comment_text.strip(),
            created_by=request.user
        )
        return JsonResponse({
            'success': True,
            'comment': comment.comment,
            'created_by': comment.created_by.username,
            'created_at': comment.create_at.strftime('%d %b %Y %H:%M')
        })
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})


# =====================================================
# 🎤 AJAX: Add Voice
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_voice(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})

    file = request.FILES['file']
    voice_obj = VoiceRecording.objects.create(
        company=company,
        file=file,
        uploaded_by=request.user
    )

    original_path = voice_obj.file.path
    compressed_path = original_path.rsplit('.', 1)[0] + "_compressed.mp3"

    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(original_path)
        audio = audio.set_frame_rate(22050).set_channels(1)
        audio.export(compressed_path, format="mp3", bitrate="64k")

        with open(compressed_path, 'rb') as f:
            voice_obj.file.save(os.path.basename(compressed_path), File(f), save=True)

        os.remove(original_path)
        os.remove(compressed_path)

        return JsonResponse({
            'success': True,
            'file_url': voice_obj.file.url,
            'uploaded_by': voice_obj.uploaded_by.username,
            'uploaded_at': voice_obj.uploaded_at.strftime('%d %b %Y %H:%M')
        })
    except Exception as e:
        print("Compression error:", e)
        return JsonResponse({
            'success': True,
            'file_url': voice_obj.file.url,
            'uploaded_by': voice_obj.uploaded_by.username,
            'uploaded_at': voice_obj.uploaded_at.strftime('%d %b %Y %H:%M'),
            'warning': 'Compression failed, original file used'
        })


# =====================================================
# ⚡ AJAX: Update Status
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_update_status(request, pk):
    company = get_object_or_404(Company, pk=pk)
    new_status = request.POST.get('status')
    if new_status:
        company.status = new_status
        company.save(update_fields=['status'])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid status'})


# =====================================================
# 📝 AJAX: Add Visit
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_visit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = VisitForm(request.POST)
    if form.is_valid():
        visit = form.save(commit=False)
        visit.company = company
        visit.uploaded_by = request.user
        visit.save()
        return JsonResponse({
            'success': True,
            'visit_for': visit.visit_for,
            'visit_type': visit.visit_type,
            'visit_status': visit.visit_status,
            'comment': visit.comment or '',
            'uploaded_at': visit.uploaded_at.strftime('%d %b %Y %H:%M')
        })
    return JsonResponse({'success': False, 'errors': form.errors})



# =================================================================
# 📅 COMPANY MEETING VIEW (Full Filter + Table)
# =================================================================

class CompanyMeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'dashboard/meeting/company_meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 20
    ordering = ['-create_at']

    def get_queryset(self):
        qs = (
            Meeting.objects.select_related(
                'company', 'company__city', 'company__locality',
                'company__category', 'assigned_to'
            )
            .order_by('-create_at')
        )

        # --- Filters ---
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        city = self.request.GET.get('city')
        locality = self.request.GET.get('locality')
        status = self.request.GET.get('status')
        assigned = self.request.GET.get('assigned_to')
        category = self.request.GET.get('category')

        if date_from:
            try:
                qs = qs.filter(meeting_date__date__gte=datetime.strptime(date_from, "%Y-%m-%d"))
            except ValueError:
                pass
        if date_to:
            try:
                qs = qs.filter(meeting_date__date__lte=datetime.strptime(date_to, "%Y-%m-%d"))
            except ValueError:
                pass
        if city:
            qs = qs.filter(company__city_id=city)
        if locality:
            qs = qs.filter(company__locality_id=locality)
        if status:
            qs = qs.filter(status=status)
        if assigned:
            qs = qs.filter(assigned_to_id=assigned)
        if category:
            qs = qs.filter(company__category_id=category)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cities'] = City.objects.all()
        ctx['localities'] = Locality.objects.all()
        ctx['staff_list'] = Staff.objects.all()
        ctx['categories'] = Category.objects.all()
        ctx['statuses'] = [s[0] for s in Meeting.MEETING_STATUS_CHOICES]
        return ctx

    model = Meeting
    template_name = 'business/company_meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 20
    ordering = ['-create_at']

    def get_queryset(self):
        qs = (
            Meeting.objects.select_related(
                'company', 'company__city', 'company__locality', 'company__category', 'assigned_to'
            ).order_by('-create_at')
        )

        # --- Filters ---
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        city = self.request.GET.get('city')
        locality = self.request.GET.get('locality')
        status = self.request.GET.get('status')
        assigned = self.request.GET.get('assigned_to')
        category = self.request.GET.get('category')

        if date_from:
            try:
                qs = qs.filter(meeting_date__date__gte=datetime.strptime(date_from, "%Y-%m-%d"))
            except ValueError:
                pass
        if date_to:
            try:
                qs = qs.filter(meeting_date__date__lte=datetime.strptime(date_to, "%Y-%m-%d"))
            except ValueError:
                pass

        if city:
            qs = qs.filter(company__city_id=city)
        if locality:
            qs = qs.filter(company__locality_id=locality)
        if status:
            qs = qs.filter(status=status)
        if assigned:
            qs = qs.filter(assigned_to_id=assigned)
        if category:
            qs = qs.filter(company__category_id=category)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cities'] = City.objects.all()
        ctx['localities'] = Locality.objects.all()
        ctx['staff_list'] = Staff.objects.all()
        ctx['categories'] = Category.objects.all()
        ctx['statuses'] = [s[0] for s in Meeting.MEETING_STATUS_CHOICES]
        return ctx