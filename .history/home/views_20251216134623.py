from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# ✅ Models and Forms
from business.models import Meeting as CompanyMeeting, Company
from business.forms import MeetingForm as BusinessMeetingForm, CompanyForm
from response.models import Meeting as ResponseMeeting, Staff
from response.forms import MeetingForm as ResponseMeetingForm
from utility.models import City, Locality, Category,Sub_Locality

from django.http import JsonResponse

def get_localities(request):
    city_id = request.GET.get("city_id")
    localities = Locality.objects.filter(city_id=city_id).values("id", "title")
    return JsonResponse(list(localities), safe=False)

def get_sub_localities(request):
    locality_id = request.GET.get("locality_id")
    sub_localities = Sub_Locality.objects.filter(locality_id=locality_id).values("id", "title")
    return JsonResponse(list(sub_localities), safe=False)



# 🏢 Edit Company Meeting (Business)
@login_required
def edit_company_meeting(request, pk):
    """Edit both the Company and its linked Meeting in one page."""
    meeting = get_object_or_404(CompanyMeeting, pk=pk)
    company = meeting.company

    if request.method == 'POST':
        # ✅ Use prefixes to prevent field name clashes
        meeting_form = BusinessMeetingForm(request.POST, prefix='meeting', instance=meeting)
        company_form = CompanyForm(request.POST, request.FILES, prefix='company', instance=company)

        if meeting_form.is_valid() and company_form.is_valid():
            # --- Save Company ---
            company_obj = company_form.save(commit=False)
            company_obj.updated_by = request.user
            company_obj.save()

            # --- Save Meeting ---
            meeting_obj = meeting_form.save(commit=False)
            meeting_obj.updated_by = request.user
            meeting_obj.company = company_obj
            meeting_obj.save()

            messages.success(
                request,
                f"✅ Meeting #{meeting.id} and Company '{company.company_name}' updated successfully!"
            )
            return redirect('company_meetings')
        else:
            messages.error(request, "❌ Please fix the form errors below.")
    else:
        meeting_form = BusinessMeetingForm(instance=meeting, prefix='meeting')
        company_form = CompanyForm(instance=company, prefix='company')

    return render(request, 'business/edit_meeting.html', {
        'meeting_form': meeting_form,
        'company_form': company_form,
        'meeting': meeting,
        'company': company,
        'title': f"Edit Company Meeting #{meeting.id}",
    })


# 📊 Edit Response Meeting
@login_required
def edit_response_meeting(request, pk):
    meeting = get_object_or_404(ResponseMeeting, pk=pk)

    if request.method == 'POST':
        form = ResponseMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            messages.success(request, f"✅ Response Meeting #{meeting.id} updated successfully!")
            return redirect('response_meetings')
        else:
            messages.error(request, "❌ Please fix the form errors below.")
    else:
        form = ResponseMeetingForm(instance=meeting)

    return render(request, 'response/edit_meeting.html', {
        'form': form,
        'title': f"Edit Response Meeting #{meeting.id}",
        'meeting': meeting,
        'type': 'response'
    })


# 📊 Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Summary Cards
        context.update({
            'total_company_meetings': CompanyMeeting.objects.count(),
            'total_response_meetings': ResponseMeeting.objects.count(),
            'total_leads': 5240,
            'completed_responses': 1280,
            'pending_followups': 48,
            'total_revenue': "5.6M",
        })

        # Meeting Grouping by Date
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)
        valid_statuses = ['New Meeting', 'Re Meeting']

        context['company_not_managed'] = CompanyMeeting.objects.filter(meeting_date__lt=today, status__in=valid_statuses)
        context['company_today'] = CompanyMeeting.objects.filter(meeting_date__date=today, status__in=valid_statuses)
        context['company_tomorrow'] = CompanyMeeting.objects.filter(meeting_date__date=tomorrow, status__in=valid_statuses)
        context['company_upcoming'] = CompanyMeeting.objects.filter(meeting_date__date__gt=tomorrow, status__in=valid_statuses)

        context['response_not_managed'] = ResponseMeeting.objects.filter(meeting_date__lt=today, status__in=valid_statuses)
        context['response_today'] = ResponseMeeting.objects.filter(meeting_date__date=today, status__in=valid_statuses)
        context['response_tomorrow'] = ResponseMeeting.objects.filter(meeting_date__date=tomorrow, status__in=valid_statuses)
        context['response_upcoming'] = ResponseMeeting.objects.filter(meeting_date__date__gt=tomorrow, status__in=valid_statuses)

        return context


# 📋 Company Meeting List View
def company_meeting_list(request, filter_type=None):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    valid_status = ['New Meeting', 'Re Meeting']

    qs = CompanyMeeting.objects.filter(status__in=valid_status)
    title = "All Company Meetings"

    if filter_type == 'not-managed':
        qs = qs.filter(meeting_date__lt=today)
        title = "❌ Not Managed Company Meetings"
    elif filter_type == 'today':
        qs = qs.filter(meeting_date__date=today)
        title = "📅 Today's Company Meetings"
    elif filter_type == 'tomorrow':
        qs = qs.filter(meeting_date__date=tomorrow)
        title = "🌤️ Tomorrow's Company Meetings"
    elif filter_type == 'upcoming':
        qs = qs.filter(meeting_date__date__gt=tomorrow)
        title = "🚀 Upcoming Company Meetings"

    # Filters
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    city = request.GET.get("city")
    locality = request.GET.get("locality")
    category = request.GET.get("category")
    assigned_to = request.GET.get("assigned_to")
    status = request.GET.get("status")

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
    if category:
        qs = qs.filter(company__category_id=category)
    if assigned_to:
        qs = qs.filter(assigned_to_id=assigned_to)
    if status:
        qs = qs.filter(status=status)

    qs = qs.select_related('company', 'company__city', 'company__locality', 'company__category', 'assigned_to').distinct()

    return render(request, 'business/meeting_list.html', {
        "meetings": qs,
        "title": title,
        "type": "company",
        "cities": City.objects.all(),
        "localities": Locality.objects.all(),
        "categories": Category.objects.all(),
        "staff_list": Staff.objects.all(),
        "statuses": [s[0] for s in CompanyMeeting.MEETING_STATUS_CHOICES],
    })


# 📊 Filtered Response Meetings Page
def response_meeting_list(request, filter_type):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    valid_status = ['New Meeting', 'Re Meeting']

    if filter_type == 'not-managed':
        meetings = ResponseMeeting.objects.filter(meeting_date__lt=today, status__in=valid_status)
        title = "❌ Not Managed Response Meetings"
    elif filter_type == 'today':
        meetings = ResponseMeeting.objects.filter(meeting_date__date=today, status__in=valid_status)
        title = "📅 Today's Response Meetings"
    elif filter_type == 'tomorrow':
        meetings = ResponseMeeting.objects.filter(meeting_date__date=tomorrow, status__in=valid_status)
        title = "🌤️ Tomorrow's Response Meetings"
    elif filter_type == 'upcoming':
        meetings = ResponseMeeting.objects.filter(meeting_date__date__gt=tomorrow, status__in=valid_status)
        title = "🚀 Upcoming Response Meetings"
    else:
        meetings = ResponseMeeting.objects.none()
        title = "No Meetings Found"

    return render(request, 'response/meeting_list.html', {
        'meetings': meetings,
        'title': title,
        'type': 'response',
    })


# 🏠 Optional: Dashboard Index

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        # ======================
        # SEARCH PARAMS
        # ======================
        query = self.request.GET.get("q")
        city_id = self.request.GET.get("city")
        category_id = self.request.GET.get("category")

        companies = Company.objects.filter(is_active=True)

        if query:
            companies = companies.filter(company_name__icontains=query)

        if city_id:
            companies = companies.filter(city_id=city_id)

        if category_id:
            companies = companies.filter(category_id=category_id)

        # ======================
        # CONTEXT (AS REQUESTED)
        # ======================
        context.update({
            "cities": City.objects.all(),
            "categories": Category.objects.all()[:12],
            "featured_companies": Company.objects.filter(
                is_active=True,
                is_featured=True
            )[:6],

            # SEARCH RESULT
            "companies": companies,
            "search_query": query,
            "selected_city": city_id,
            "selected_category": category_id,
        })

        return context

