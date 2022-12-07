# Create your models here.
from django.db import models
from django_config import settings

# Create your models here.
class CvBasic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    content = models.TextField()
    
    def __str__(self):
        return '%s -- %s' % (self.name, self.user)