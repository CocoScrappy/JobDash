from django.db import models
from datetime import datetime
from cv import models as cv_models

# Create your models here.
class Application(models.Model):
    STATUSES = [
        ('screening', 'Screening'),
        ('technical', 'Technical'),
        ('managerial', 'Managerial'),
        ('offer', 'Offer'),
        ('accepted', 'Accepted'),
    ]
     
    job_posting = models.ForeignKey('job_posting.Job_posting', related_name='applications', on_delete=models.SET_NULL)
    cv = models.ForeignKey(cv_models.CV, related_name='applications', on_delete=models.SET_NULL)
    
    application_date = models.DateTimeField(default=datetime.now())
    notes = models.TextField(blank=True, max_length=2500)
    favorited = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=30,
        choices=STATUSES,
    )
    