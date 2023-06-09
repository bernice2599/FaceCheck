# Generated by Django 4.0.2 on 2022-11-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_classroom_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='consent',
            field=models.BooleanField(default=False, verbose_name='Consent'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='consent',
            field=models.BooleanField(default=False, verbose_name='Consent'),
        ),
    ]
