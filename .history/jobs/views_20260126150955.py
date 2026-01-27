# jobs/views.py
from django.shortcuts import render, redirect
from .forms import JobForm

def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("jobs_home")
    else:
        form = JobForm()

    return render(request, "jobs/create_job.html", {"form": form})
