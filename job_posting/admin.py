from django.contrib import admin
from job_posting.models import JobPost
# Register your models here.

class JobPostingAdmin(admin.ModelAdmin):
    pass

admin.site.register(JobPost,JobPostingAdmin)