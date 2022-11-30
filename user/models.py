from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,role,summary=None,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email=self.normalize_email(email)
        email=email.lower()

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self,first_name,last_name,email,role,summary=None,password=None):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            role=role
        )
        user.set_password(password)
        user.summary=""
        user.is_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = [
        ('user', 'User'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=250, unique=True)
    summary = models.CharField(max_length=500,default="", blank=True)
    password = models.CharField(max_length=250)
    role = models.CharField(
        max_length=15,
        choices=USER_ROLES,
        default= 'user',
    )
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    objects=UserAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','role']

    def __str__(self):
        return "Name: {first_name} {last_name}; Email: {email}".format(first_name = self.first_name, last_name = self.last_name, email = self.email)

