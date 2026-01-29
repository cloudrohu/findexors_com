from django.contrib import admin
from .models import (
    JobTitle,
    JobCategory,
    JobIndustry,
    JobSkill,
    JobBenefit,
    JobAsset,
    JobDocument,
    JobLanguageRequirement,
    SalaryType,
    WorkingDaysOption,
    JobTimingTemplate,
)

# =====================================================
# 🔹 BASE ADMIN (Reuse)
# =====================================================
class BaseUtilityAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ("name",)
    ordering = ("name",)


# =====================================================
# 🔹 JOB TITLE
# =====================================================
@admin.register(JobTitle)
class JobTitleAdmin(BaseUtilityAdmin):
    list_display = ("id", "name", "is_active")
    list_filter = ("is_active",)


# =====================================================
# 🔹 JOB CATEGORY
# =====================================================
# admin.py
@admin.register(JobCategory)
class JobCategoryAdmin(BaseUtilityAdmin):
    # Change 'jobtitle' back to 'job_title' to match your model definition
    list_display = ("id", "name", "job_title") 
    list_filter = ("job_title",)
    fields = ("job_title", "name")

# =====================================================
# 🔹 JOB INDUSTRY
# =====================================================
@admin.register(JobIndustry)
class JobIndustryAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 JOB SKILL
# =====================================================
@admin.register(JobSkill)
class JobSkillAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 JOB BENEFIT
# =====================================================
@admin.register(JobBenefit)
class JobBenefitAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 JOB ASSET
# =====================================================
@admin.register(JobAsset)
class JobAssetAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 JOB DOCUMENT
# =====================================================
@admin.register(JobDocument)
class JobDocumentAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 LANGUAGE REQUIREMENT
# =====================================================
@admin.register(JobLanguageRequirement)
class JobLanguageRequirementAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 SALARY TYPE
# =====================================================
@admin.register(SalaryType)
class SalaryTypeAdmin(BaseUtilityAdmin):
    list_display = ("id", "name")


# =====================================================
# 🔹 WORKING DAYS OPTION
# =====================================================
@admin.register(WorkingDaysOption)
class WorkingDaysOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "label")
    search_fields = ("label",)
    ordering = ("label",)


# =====================================================
# 🔹 JOB TIMING TEMPLATE
# =====================================================
@admin.register(JobTimingTemplate)
class JobTimingTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time")
    ordering = ("start_time",)
