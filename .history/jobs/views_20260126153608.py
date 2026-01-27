# jobs/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import JobForm
from utility.models import Locality


# ==============================
# AJAX: Load localities by city
# ==============================
def ajax_load_localities(request):
    city_id = request.GET.get("city_id")

    localities = Locality.objects.filter(
        city_id=city_id
    ).order_by("name")

    data = [
        {"id": loc.id, "name": loc.name}
        for loc in localities
    ]

    return JsonResponse(data, safe=False)


# ==============================
# Create Job
# ==============================
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")   # ✅ TEMP SAFE REDIRECT
        else:
            # 🔥 VERY IMPORTANT: Debug errors
            print("JOB FORM ERRORS 👉", form.errors)

    else:
        form = JobForm()

    return render(
        request,
        "jobs/create_job.html",
        {"form": form}
    )
