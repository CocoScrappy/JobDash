from django.db import models

# Create your models here.
class Applicant(models.Model):
    USER_ROLES = [
        ('applicant', 'Applicant'),
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
        default= 'applicant',
    )
    
    def __str__(self):
        return "Name: {firstname} {lastname}; Email: {email}".format(self.firstname, self.lastname, self.email)