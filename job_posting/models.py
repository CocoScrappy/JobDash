import re
from django.db import models
from datetime import datetime, timedelta
from django_config import settings

# Create your models here.


class JobPost(models.Model):

    def __str__(self):
        return self.title

    REMOTE_OPTIONS = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('in-person', 'In-Person'),
    ]

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    title = models.CharField(
        max_length=250, help_text="This title cannot exceed 250 chars")
    logo_url = models.URLField(null=True)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=False)
    company = models.CharField(max_length=60, default='', blank=True)
    date_created = models.DateTimeField(default=datetime.now())
    link = models.URLField(null=True)

    remote_option = models.CharField(
        max_length=30,
        choices=REMOTE_OPTIONS,
    )

    def calculatePostDate(daysAgoStr):
        if daysAgoStr.lower() != "today":
            daysAgoInt = int(re.sub(r'[^0-9]', '', daysAgoStr.split()[0]))
            datePosted = datetime.today() - timedelta(days=daysAgoInt)
        else:
            datePosted = datetime.today()

        return datePosted.isoformat()


class Skill(models.Model):
    name = models.CharField(max_length=250, unique=True)
