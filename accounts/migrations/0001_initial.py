# Generated by Django 4.1.2 on 2022-10-27 23:52

import accounts.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False, verbose_name='student status')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='teacher status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=50, verbose_name='Subject Name')),
                ('code', models.SlugField(default=accounts.models.random_string, max_length=10, unique=True, verbose_name='Subject Code')),
                ('created_timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Classroom',
                'verbose_name_plural': 'Classrooms',
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Stream Name')),
            ],
            options={
                'verbose_name': 'stream',
                'verbose_name_plural': 'streams',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Class Name')),
                ('year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MaxValueValidator(2030), django.core.validators.MinValueValidator(2015)])),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='accounts.stream')),
            ],
            options={
                'verbose_name': 'class',
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('course', models.CharField(max_length=200, null=True)),
                ('grade_year', models.CharField(max_length=200, null=True)),
                ('block_section', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(default='Absent', max_length=200, null=True)),
                ('sub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='accounts.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teachers', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tech_picture', models.ImageField(blank=True, null=True, upload_to=accounts.models.tech_directory_path)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='accounts.stream')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
            },
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='accounts.teacher'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='students', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('roll_no', models.PositiveIntegerField(verbose_name='Roll No.')),
                ('student_id', models.CharField(max_length=50, unique=True, verbose_name='Student ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=accounts.models.stud_directory_path)),
                ('classrooms', models.ManyToManyField(blank=True, related_name='students', to='accounts.classroom')),
                ('current_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='accounts.class', verbose_name='Class')),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
                'unique_together': {('roll_no', 'current_class')},
            },
        ),
    ]
