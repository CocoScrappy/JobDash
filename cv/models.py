from django.db import models
from django_config import settings

# Create your models here.
class CV(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return '%s' % (self.name)
    
class CV_elements(models.Model):
    CV_SECTIONS = [
        ('experience', 'Experience'),
        ('education', 'Education'),
        ('projects', 'Projects'),
        ('skills', 'Skills'),
        ('languages', 'Languages'),
        ('certificates', 'Certificates'),
    ]
    
    cv = models.ForeignKey(CV, related_name='cv_elements', on_delete=models.CASCADE)
    title = models.CharField(max_length= 120, null=True)
    organization = models.CharField(max_length= 250, null=True)
    location = models.CharField(max_length= 60, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    content = models.TextField(max_length=2500, null=False)
    url = models.URLField(null=True)
    section = models.CharField(
        max_length=30,
        choices=CV_SECTIONS,
    )
    
    def __str__(self):
        return '%s: %s' % (self.section, self.title)