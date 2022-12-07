# Generated by Django 4.1.3 on 2022-12-07 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0015_skill_alter_jobpost_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='isSkill',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 12, 17, 21, 469741)),
        ),
    ]
