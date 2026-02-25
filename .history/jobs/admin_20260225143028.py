from django.contrib import admin
from .models import Job, JobApplicant, InterviewSchedule


# =====================================================
# INTERVIEW INLINE
# =====================================================
class InterviewInline(admin.StackedInline):
    model = InterviewSchedule
    extra = 0
    max_num = 1
    can_delete = True

    readonly_fields = ("created_at", "updated_at", "job")

    fieldsets = (
        ("Interview Details", {
            "fields": (
                "scheduled_datetime",
                "interview_type",
                "duration_minutes",
                "rescheduled_from",
            )
        }),
        ("Assignment", {
            "fields": (
                "assigned_to",
                "status",
            )
        }),
        ("Tracking", {
            "fields": (
                "whatsapp_sent",
                "reminder_sent",
                "confirmation_received",
            )
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
        }),
    )


# =====================================================
# JOB APPLICANT INLINE (INSIDE JOB)
# =====================================================
class JobApplicantInline(admin.TabularInline):
    model = JobApplicant
    extra = 0
    show_change_link = True
    readonly_fields = ("applied_at",)

    fields = (
        "full_name",
        "phone",
        "city",
        "experience_months",
        "status",
        "apply_source",
        "applied_at",
    )


# =====================================================
# JOB ADMIN
# =====================================================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "company",
        "category",
        "industry",
        "job_type",
        "work_location_type",
        "city",
        "locality",
        "gender",
        "salary_type",
        "salary_min",
        "salary_max",
        "openings",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "company",
        "category",
        "industry",
        "job_type",
        "work_location_type",
        "gender",
        "salary_type",
        "city",
        "locality",
        "working_days",
        "created_at",
    )

    search_fields = (
        "title__name",
        "company__company_name",
        "city__name",
        "locality__name",
    )

    autocomplete_fields = (
        "company",
        "title",
        "industry",
        "city",
        "locality",
        "working_days",
        "created_by",
        "updated_by",
    )

    list_select_related = (
        "company",
        "title",
        "industry",
        "city",
        "locality",
    )

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    readonly_fields = ("slug", "created_at", "updated_at")

    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "company",
                "title",
                "category",
                "industry",
                "slug",
                "openings",
                "status",
            )
        }),
        ("Location & Type", {
            "fields": (
                "job_type",
                "work_location_type",
                "city",
                "locality",
                "working_days",
                "start_time",
                "end_time",
            )
        }),
        ("Experience & Salary", {
            "fields": (
                "gender",
                "min_experience_months",
                "max_experience_months",
                "salary_type",
                "salary_min",
                "salary_max",
            )
        }),
        ("Requirements", {
            "fields": (
                "skills",
                "benefits",
                "assets",
                "documents",
                "languages",
                "description",
                "requirements",
            )
        }),
        ("Meta", {
            "fields": (
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            )
        }),
    )
    readonly_fields = (
        "slug",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    inlines = [JobApplicantInline]


# =====================================================
# JOB APPLICANT ADMIN
# =====================================================
@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):

    change_list_template = "admin/jobs/jobapplicant/change_list.html"

    list_display = (
        "id",
        "full_name",
        "job",
        "phone",
        "city",
        "locality",
        "experience_months",
        "current_salary",
        "expected_salary",
        "notice_period",
        "apply_source",
        "allow_whatsapp",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "apply_source",
        "job",
        "city",
        "locality",
        "notice_period",
        "allow_whatsapp",
        "applied_at",
        "status_updated_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "current_company",
        "job__title__name",
    )

    autocomplete_fields = (
        "job",
        "city",
        "locality",
        "user",
    )

    list_select_related = (
        "job",
        "city",
        "locality",
        "user",
    )

    readonly_fields = (
        "applied_at",
        "status_updated_at",
    )

    date_hierarchy = "applied_at"

    inlines = [InterviewInline]

    # 🔥 SMART SEARCH
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("JA"):
                num = term.replace("JA", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("JOB"):
                num = term.replace("JOB", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(job__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(phone__icontains=term)

        return queryset, use_distinct


# =====================================================
# INTERVIEW ADMIN
# =====================================================
@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):

    change_list_template = "admin/jobs/interviewschedule/change_list_cards.html"
    preserve_filters = True
    list_per_page = 50

    list_display = (
        "id",
        "applicant",
        "job",
        "interview_type",
        "scheduled_datetime",
        "assigned_to",
        "status",
        "whatsapp_sent",
        "confirmation_received",
    )

    list_filter = (
        "status",
        "interview_type",
        "assigned_to",
        "job",
        "whatsapp_sent",
        "reminder_sent",
        "confirmation_received",
        "scheduled_datetime",
        "created_at",
    )

    search_fields = (
        "applicant__full_name",
        "applicant__phone",
        "job__title__name",
    )

    autocomplete_fields = (
        "applicant",
        "assigned_to",
    )

    list_select_related = (
        "applicant",
        "job",
        "assigned_to",
    )

    readonly_fields = (
        "job",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "scheduled_datetime"
    ordering = ("-scheduled_datetime",)

    fieldsets = (
        ("Candidate & Assignment", {
            "fields": (
                "applicant",
                "job",
                "assigned_to",
            )
        }),
        ("Schedule Details", {
            "fields": (
                "scheduled_datetime",
                "interview_type",
                "duration_minutes",
                "rescheduled_from",
            )
        }),
        ("Meeting Info", {
            "fields": (
                "meeting_link",
                "location",
            )
        }),
        ("Status & CRM", {
            "fields": (
                "status",
                "remarks",
                "internal_feedback",
                "whatsapp_sent",
                "reminder_sent",
                "confirmation_received",
                "last_contacted_at",
                "next_followup_at",
            )
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    # 🔥 MAGIC SEARCH
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            term = search_term.upper().strip()

            if term.startswith("INT"):
                num = term.replace("INT", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(id=int(num))

            if term.startswith("APP"):
                num = term.replace("APP", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(applicant__id=int(num))

            if term.startswith("JOB"):
                num = term.replace("JOB", "").lstrip("0")
                if num.isdigit():
                    queryset |= self.model.objects.filter(job__id=int(num))

            if term.isdigit():
                queryset |= self.model.objects.filter(applicant__phone__icontains=term)

        return queryset, use_distinct
