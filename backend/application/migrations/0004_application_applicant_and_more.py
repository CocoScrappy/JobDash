# Generated by Django 4.1.3 on 2022-11-22 17:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('application', '0003_alter_application_application_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='applications', to='user.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='application_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 22, 12, 51, 23, 571623)),
        ),
    ]
