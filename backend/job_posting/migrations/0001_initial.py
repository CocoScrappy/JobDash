# Generated by Django 4.1.3 on 2022-11-22 23:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('logo_url', models.URLField(blank=True)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2022, 11, 22, 18, 10, 54, 128751))),
                ('remote_option', models.CharField(choices=[('remote', 'Remote'), ('hybrid', 'Hybrid'), ('in-person', 'In-Person')], max_length=30)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='postings', to='user.user')),
            ],
        ),
    ]
