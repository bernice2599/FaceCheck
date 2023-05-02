from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *

class StudentForm(UserCreationForm):

    email = forms.EmailField(label='Email', required=True)

    picture = forms.ImageField(label = 'Picture', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)
    
    student_id = forms.CharField(label='Student ID', max_length=50, required=True, min_length=4)
    
    consent = forms.BooleanField(label='Consent', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        field = ('first_name', 'last_name','username', 'email','password1', 'password2', 'picture', 'consent')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.consent = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        student = Student.objects.create(
            user=user,
            student_id = self.cleaned_data['student_id'],  
            picture =  self.cleaned_data['picture'],
            )
        student.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        student_id = self.cleaned_data.get('student_id')
        email = self.cleaned_data.get('email')
    
        # Student id validation
        if Student.objects.filter(student_id=student_id).exists():
            print("Student ID exists")
            raise forms.ValidationError('Student with Student ID already exists.')
        
        # Email Validations
        if User.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError('User with Email already exists.')


class TeacherForm(UserCreationForm):

    email = forms.EmailField(label='Email', required=True)

    tech_picture = forms.ImageField(label = 'Picture', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)

    consent = forms.BooleanField(label='Consent', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        field = ('first_name', 'last_name','username', 'email','password1', 'password2', 'tech_picture','consent')


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.consent = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        teacher = Teacher.objects.create(
            user=user,
            tech_picture =  self.cleaned_data['tech_picture'],  
            )
        teacher.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')

        # Email Validations
        if User.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError('User with Email already exists.')
