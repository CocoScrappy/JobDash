from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
User=get_user_model()

class UserCreationForm(forms.ModelForm):
    pass1=forms.CharField(label='Password',widget=forms.PasswordInput)
    pass2=forms.CharField(label='Confirm Passowrd',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields= ('id','first_name', 'last_name', 'email', 'summary', 'password', 'role')

    def clean_password2(self):
        pass1=self.cleaned_data.get("pass1")
        pass2=self.cleaned_data.get("pass2")
        if pass1 and pass2 and pass1!=pass2:
            raise forms.ValidationError("Passwords don't match")
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["pass1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()
    class Meta:
        model=User
        fields= ('id','first_name', 'last_name', 'email', 'summary', 'password', 'role','is_active','is_staff')

    def clean_password(self):
        return self.initial["password"]


# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form=UserCreationForm

    list_display = ('email', 'first_name','last_name','role', 'is_staff')
    list_filter = ('is_staff','role')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','summary',)}),
        ('Permissions', {'fields': ('is_staff','role')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name' ,'role', 'pass1', 'pass2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
#Register model
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
