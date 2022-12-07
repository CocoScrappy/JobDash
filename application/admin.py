from django.contrib import admin
from application.models import Application, Saved_Date

# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    #list_display = '__all__'
    pass

class DateAdmin(admin.ModelAdmin):
    #list_display = '__all__'
    pass

# Register model
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Saved_Date, DateAdmin)
