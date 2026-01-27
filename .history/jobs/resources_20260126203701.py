from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import JobApplicant, Job
from utility.models import City, Locality


class JobApplicantResource(resources.ModelResource):

    job = fields.Field(
        column_name="job_id",
        attribute="job",
        widget=ForeignKeyWidget(Job, "id")
    )

    city = fields.Field(
        column_name="city",
        attribute="city",
        widget=ForeignKeyWidget(City, "name")
    )

    locality = fields.Field(
        column_name="locality",
        attribute="locality",
        widget=ForeignKeyWidget(Locality, "name")
    )

    class Meta:
        model = JobApplicant
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("job", "phone")  # duplicate se bachaata hai
        fields = (
            "id",
            "job",
            "full_name",
            "phone",
            "email",
            "city",
            "locality",
            "experience_months",
            "current_company",
            "current_salary",
            "expected_salary",
            "notice_period",
            "status",
            "apply_source",
            "applied_at",
        )
