from django.db import models
from datetime import datetime
from cv_basic import models as cv_models
from job_posting.models import JobPost
from django_config import settings

# Create your models here.
class Application(models.Model):
    STATUSES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('technical', 'Technical'),
        ('managerial', 'Managerial'),
        ('offer', 'Offer'),
        ('accepted', 'Accepted'),
    ]
     
    job_posting = models.ForeignKey(JobPost, related_name='applications', on_delete=models.DO_NOTHING)
    cv = models.ForeignKey(cv_models.CvBasic, related_name='applications', on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    
    application_date = models.DateTimeField(default=datetime.now())
    notes = models.TextField(blank=True, max_length=2500)
    favorited = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=30,
        choices=STATUSES,
    )
    