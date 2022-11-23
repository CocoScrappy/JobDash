from django.db import models

# Create your models here.
from django.db import models
from user.models import User

# Create your models here.
class CvBasic(models.Model):
    user = models.ForeignKey(User, related_name='cvs', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    content = models.TextField()
    
    def __str__(self):
        return '%s' % (self.name)