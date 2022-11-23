from django.contrib import admin
from .models import Applicant

# Register your models here.
class ApplicantAdmin(admin.ModelAdmin):
    list_disply = ('firstname', 'lastname', 'email', 'summary', 'password', 'role')
    
#Register model
admin.site.register(Applicant, ApplicantAdmin)