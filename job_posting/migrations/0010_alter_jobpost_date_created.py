# Generated by Django 4.1.3 on 2022-12-04 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0009_alter_jobpost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 4, 13, 20, 13, 122369)),
        ),
    ]
