from django.db import models

# Create your models here.
class JobTitle(models.Model):
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class JobCategory(models.Model):
    jobtitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE,null=True,blank=True,related_name="jobtitle")

    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class JobIndustry(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class JobSkill(models.Model):
    jobtitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE,null=True,blank=True,related_name="jobtitle")

    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class JobBenefit(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class JobAsset(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class JobDocument(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class JobLanguageRequirement(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class SalaryType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WorkingDaysOption(models.Model):
    label = models.CharField(max_length=150)

    def __str__(self):
        return self.label



class JobTimingTemplate(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
