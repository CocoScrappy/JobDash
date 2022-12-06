# Generated by Django 4.1.3 on 2022-12-06 03:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_rename_date_saved_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 5, 22, 35, 41, 947663)),
        ),
        migrations.AlterField(
            model_name='saved_date',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_dates', to='application.application'),
        ),
    ]
