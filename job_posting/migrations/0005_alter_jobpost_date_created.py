# Generated by Django 4.1.3 on 2022-11-28 16:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0004_jobpost_company_alter_jobpost_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 11, 55, 59, 571371)),
        ),
    ]