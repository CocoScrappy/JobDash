# Generated by Django 4.1.3 on 2022-11-24 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0003_alter_jobpost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 24, 12, 56, 7, 591423)),
        ),
    ]