from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_disply = ('firstname', 'lastname', 'email', 'summary', 'password', 'role')
    
#Register model
admin.site.register(User, UserAdmin)
