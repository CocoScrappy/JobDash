# Generated by Django 4.1.3 on 2022-11-22 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('summary', models.CharField(max_length=500, null=True)),
                ('password', models.CharField(max_length=250)),
                ('role', models.CharField(choices=[('user', 'User'), ('employer', 'Employer'), ('admin', 'Admin')], default='user', max_length=15)),
            ],
        ),
    ]