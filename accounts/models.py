from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from django.urls import reverse
from django.utils import timezone, text
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import datetime
from time import time
import random
import string
from PIL import Image

def _(something):
    return something

def stud_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.user.username # + "_" + instance.username
    filename = name +'.'+ ext 
    return 'student_images/{}'.format(filename)

def tech_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.user.username # + "_" + instance.username
    filename = name +'.'+ ext 
    return 'teacher_images/{}'.format(filename)

class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teachers')
    tech_picture=models.ImageField(upload_to=tech_directory_path, blank = True, null = True )
    consent = models.BooleanField('Consent', default=False)

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.pk})

def random_string(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Classroom(models.Model):
    id=models.AutoField(primary_key=True)
    teacher = models.ForeignKey( "Teacher", on_delete=models.CASCADE, blank=False, related_name='classrooms')
    subject = models.CharField(_("Subject Name"), max_length=50, blank=False)
    code = models.SlugField(_("Subject Code"), max_length=5, default=random_string, unique=True)
    created_timestamp = models.DateTimeField( default=timezone.now, editable=False)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Classroom")
        verbose_name_plural = _("Classrooms")

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("Classroom_detail", kwargs={"pk": self.pk})

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='students')
    student_id = models.CharField(_("Student ID"), max_length=50, blank=False, unique=True)
    classrooms = models.ManyToManyField("Classroom", related_name='students', blank=True)
    picture=models.ImageField(upload_to=stud_directory_path, blank = True, null = True )
    consent = models.BooleanField('Consent', default=False)
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    student_no =  models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    grade_year = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    block_section = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    sub = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    course = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')
    status = models.CharField(max_length=200, null = True, default='Absent')
    category = models.CharField(max_length=200, null=False, blank=False, default='Forgotten')

    def __str__(self):
        return str(self.student_name + "_" + str(self.date)+ "_" + str(self.subject))

def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.registration_id # + "_" + instance.course + "_" + instance.year + "_" + instance.block
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}/{}'.format(instance.course,instance.year,instance.block,filename)

class FTF_Student(models.Model):

    COURSE = (
        ('BIO','BIO'),
        ('IT','IT'),
        ('CS','CS'),
        ('CHEM','CHEM'),
        ('MET','MET'),
    )
    YEAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    )
    BLOCK = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    )

    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True)
    course = models.CharField(max_length=100, null=True, choices=COURSE)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    block = models.CharField(max_length=100, null=True, choices=BLOCK)
    profile_pic = models.ImageField(upload_to=student_directory_path ,null=True, blank=True)

    def __str__(self):
        return str(self.registration_id)

class FTF_Attendance(models.Model):
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    course = models.CharField(max_length=200, null = True)
    year = models.CharField(max_length=200, null = True)
    block = models.CharField(max_length=200, null = True)
    subject = models.CharField(max_length=200, null = True)
    period = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=200, null = True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date)+ "_" + str(self.period))