from django.db import models
from datetime import datetime
from django_config import settings

# Create your models here.
class JobPost(models.Model):
    REMOTE_OPTIONS = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('in-person', 'In-Person'),
    ]
     
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    
    title = models.CharField(max_length=250)
    logo_url = models.URLField(blank=True)
    location = models.CharField(max_length= 100)
    description = models.TextField(blank=False)
    date_created = models.DateTimeField(default=datetime.now())
    
    remote_option = models.CharField(
        max_length=30,
        choices=REMOTE_OPTIONS,
    )
    