from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobCreateForm


@login_required
def create_job(request):
    if request.method == "POST":
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.status = "active"   # or "draft"
            job.save()
            form.save_m2m()
            return redirect("job_success")
    else:
        form = JobCreateForm()

    return render(request, "jobs/create_job.html", {"form": form})
