from django.db import models

# Create your models here.
class User(models.Model):
    USER_ROLES = [
        ('user', 'User'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=250, unique=True)
    summary = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=250)
    role = models.CharField(
        max_length=15,
        choices=USER_ROLES,
        default= 'user',
    )
    
    def __str__(self):
        return "Name: {first_name} {last_name}; Email: {email}".format(first_name = self.first_name, last_name = self.last_name, email = self.email)