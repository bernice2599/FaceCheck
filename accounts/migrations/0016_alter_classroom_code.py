# Generated by Django 4.0.2 on 2022-11-17 08:44

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_attendance_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='code',
            field=models.SlugField(default=accounts.models.random_string, max_length=8, unique=True, verbose_name='Subject Code'),
        ),
    ]
