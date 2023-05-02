from accounts.models import Classroom,Teacher, Student, User
from django import forms
from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.db import transaction


class JoinClassroomForm(forms.Form):
    code = forms.CharField(max_length=50, required=True)



class AttendanceForm(forms.Form):
    student_name = forms.CharField(label='Student Name', max_length=250, required=True)

class PhotoForm(forms.ModelForm):
    class Meta:
        model=Student
        #exclude = ('student_id',)
        fields=('picture',)
    def clean_photo(self):
        picture=self.cleaned_data.get('picture')

