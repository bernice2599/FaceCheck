from accounts.models import *
from django import forms

from django.forms import ModelForm

class ClassroomForm(forms.ModelForm):
    
    class Meta:
        model = Classroom
        exclude = ('teacher','status')

class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = FTF_Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        #self.fields['firstname'].widget.attrs['class'] = 'form-control'
        #self.fields['lastname'].widget.attrs['class'] = 'form-control'
        #self.fields['registration_id'].widget.attrs['class'] = 'form-control'
        #self.fields['course'].widget.attrs['class'] = 'form-control'
        #self.fields['year'].widget.attrs['class'] = 'form-control'
        #self.fields['block'].widget.attrs['class'] = 'form-control'
        #self.fields['profile_pic'].widget.attrs['class'] = 'form-control'