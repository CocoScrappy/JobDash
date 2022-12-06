# Generated by Django 4.1.3 on 2022-12-06 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0013_alter_jobpost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 10, 44, 16, 719416)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='title',
            field=models.CharField(help_text='This title cannot exceed 250 chars', max_length=250),
        ),
    ]