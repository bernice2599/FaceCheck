# Generated by Django 4.0.2 on 2022-11-17 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_classroom_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='course',
        ),
    ]
