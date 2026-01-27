from django.shortcuts import render, redirect
from .forms import JobForm
from django.http import JsonResponse
from utility.models import Locality


def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            form.save_m2m()
            return redirect("jobs_home")
    else:
        form = JobForm()

    return render(request, "jobs/create_job.html", {"form": form})


def ajax_load_localities(request):
    city_id = request.GET.get("city_id")
    data = list(
        Locality.objects.filter(city_id=city_id)
        .values("id", "name")
    )
    return JsonResponse(data, safe=False)
