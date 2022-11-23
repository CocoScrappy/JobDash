# Generated by Django 4.1.3 on 2022-11-22 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CV_elements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True)),
                ('organization', models.CharField(max_length=250, null=True)),
                ('location', models.CharField(max_length=60, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('content', models.TextField(max_length=2500)),
                ('url', models.URLField(null=True)),
                ('section', models.CharField(choices=[('experience', 'Experience'), ('education', 'Education'), ('projects', 'Projects'), ('skills', 'Skills'), ('languages', 'Languages'), ('certificates', 'Certificates')], max_length=30)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cv_elements', to='cv.cv')),
            ],
        ),
    ]
