# Generated by Django 4.1.3 on 2022-12-05 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0007_alter_jobpost_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='link',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='company',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 5, 4, 35, 47, 707090)),
        ),
    ]
