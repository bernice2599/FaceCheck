# Generated by Django 4.0.2 on 2022-11-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_delete_photo_attendance_student_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
