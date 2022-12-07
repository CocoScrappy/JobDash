from django.contrib import admin
from cv_basic.models import CvBasic
# Register your models here.

class CvBasicAdmin(admin.ModelAdmin):
    pass

admin.site.register(CvBasic,CvBasicAdmin)