from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView
from accounts.models import *
from .models import *
from .forms import *
from accounts.passtests import StudentTestMixin, TeacherTestMixin
from .filters import *
from datetime import date
import datetime
from time import time
import xlwt
from django.contrib import messages
import os
from .recognizer import Recognizer
from .recognizer2 import Recognizer2
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
import face_recognition

class ProfileTeacherView(TeacherTestMixin, TemplateView):
    template_name = "teachers/teacherprofile.html"

def edit_profile(request):
    return render(request,"teachers/edit_profile.html")

def edit_profile_usern(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('teachers:edit_profile'))
    else:
        username=request.POST.get("username")

        try:
            customuser=User.objects.get(id=request.user.id)
            customuser.username=username
            #Username Validations
            if User.objects.filter(username=username).exists():
                messages.error(request,"User with Username already exists.")
                return HttpResponseRedirect(reverse('teachers:edit_profile'))
            else:
                customuser.save()
                messages.success(request, "Username updated.")
                return HttpResponseRedirect(reverse('teachers:teacherprofile'))
        except:
            messages.error(request,"Failed to update.")
            return HttpResponseRedirect(reverse('teachers:edit_profile'))

def edit_profile_email(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('teachers:edit_profile'))
    else:
        email=request.POST.get("email")
        
        try:
            customuser=User.objects.get(id=request.user.id)
            customuser.email=email
            #Username Validations
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists.")
                return HttpResponseRedirect(reverse('teachers:edit_profile'))
            else:
                customuser.save()
                messages.success(request, "Email updated.")
                return HttpResponseRedirect(reverse('teachers:teacherprofile'))
        except:
            messages.error(request,"Failed to update.")
            return HttpResponseRedirect(reverse('teachers:edit_profile'))

def edit_profile_info(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('teachers:edit_profile'))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")

        try:
            customuser=User.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.save()
            messages.success(request, "Profile updated.")
            return HttpResponseRedirect(reverse('teachers:teacherprofile'))
        except:
            return HttpResponseRedirect(reverse('teachers:edit_profile'))

def edit_profile_passw(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('teachers:edit_profile'))
    else:
        password=request.POST.get("password")
        try:
            customuser=User.objects.get(id=request.user.id)
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Password changed. Try to log in.")
            return redirect('accounts:home')
        except:
            return HttpResponseRedirect(reverse('teachers:edit_profile'))


class DashboardView(TeacherTestMixin,TemplateView):
    template_name = "teachers/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classrooms'] = self.request.user.teachers.classrooms.all()
        return context

def add_classroom(request):
    form = ClassroomForm()

    def form_valid(self, form):
        classroom = form.save(commit=False)
        classroom.teacher = Teacher.objects.get(user=self.request.user.teachers)
        classroom.save()
        return HttpResponseRedirect(self.get_success_url())    

def TakeAttendanceView(request,code):
    context_dict = {}
    room = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = room
    return render(request, 'teachers/take_attendance.html', context=context_dict)

class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "teachers/addclassroom.html"
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user.teachers
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('teachers:dashboard')

class ClassroomDeleteView(DeleteView):
    model = Classroom
    template_name = "teachers/deleteclassroom.html"

    # Should match the value after ':' from url <slug:the_slug>
    slug_url_kwarg = 'code'
    
    # Should match the name of the slug field on the model 
    slug_field = 'code' # DetailView's default value: optional
    
    def get_success_url(self):
        return reverse('teachers:dashboard')

def toggle_status_on(request, id):
    if request.method == 'POST':
        classroom = Classroom.objects.get(pk=id)
        classroom.status = True
        classroom.save()
        messages.success(request, "Taking attendance in student's view is on.")
    return redirect(reverse_lazy('teachers:dashboard'))

def toggle_status_off(request, id):
    if request.method == 'POST':
        classroom = Classroom.objects.get(pk=id)
        classroom.status = False
        classroom.save()
        messages.success(request, "Taking attendance in student's view is off.")
    return redirect(reverse_lazy('teachers:dashboard'))

def ClassroomDetailView(request,code):
    context_dict={}
    room = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = room
    attendances = Attendance.objects.all().order_by('date')
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    context_dict['myFilter'] = AttendanceFilter(request.GET, queryset=attendances)
    context_dict['attendances'] = myFilter.qs
    return render(request, 'teachers/classroom_detail.html', context=context_dict)

def attendance(request):
    if request.method == 'POST':
        details = {
            'student_name':request.POST['student_name'],
            'student_no':request.POST['student_no'],
            'course':request.POST['course'],
            'grade_year':request.POST['grade_year'],
            'block_section':request.POST['block_section'],
            'sub':request.POST['sub'],
            }
        if Attendance.objects.filter(student_no = details['student_no'], date = str(date.today()), course = details['course'], grade_year = details['grade_year'], block_section = details['block_section'], sub = details['sub']).count() != 0 :
            messages.error(request, "Attendance already recorded.")
            return redirect(reverse_lazy('teachers:dashboard'))
        else:
            names = Recognizer(details)
            if request.user.is_teacher:
                if request.POST['student_name'] in names:
                    attendance = Attendance(student_name = details['student_name'],
                    student_no=details['student_no'],
                    course =  details['course'],
                    grade_year = details['grade_year'], 
                    block_section = details['block_section'],
                    sub = details['sub'],
                    status = 'Present')
                    attendance.save()
                else:
                    attendance = Attendance(student_name = details['student_name'],
                    student_no=details['student_no'],
                    course =  details['course'],
                    grade_year = details['grade_year'], 
                    block_section = details['block_section'],
                    sub = details['sub'])
                    attendance.save()
            attendances = Attendance.objects.filter(date = str(date.today()), student_no = details['student_no'], course = details['course'], grade_year = details['grade_year'], block_section = details['block_section'], sub = details['sub'])
            context = {"attendances":attendances, "ta":True}
            messages.success(request, "Attendance taking Successful.")
            return render(request, 'teachers/attendance_done.html', context)        
    context = {}
    return render(request, 'teachers/classroom_detail.html', context)

def delete_attendance(request, id):
    attendance = Attendance.objects.get(pk=id)
    attendance.delete()
    messages.success(request, "Attendance deleted.")
    return redirect('teachers:dashboard')

def ClassroomStudentsView(request,code):
    context_dict = {}
    classroom = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = classroom
    context_dict['classroom_students'] = classroom.students.all()
    return render(request, template_name='teachers/classroomstudents.html', context=context_dict)

def deleting(request):
    return render(request,'teachers/delete_acc.html')
    
def delete_acc(request, id):
    user = User.objects.get(pk=id)
    if len(user.teachers.tech_picture) > 0:
        os.remove(user.teachers.tech_picture.path)
    user.delete()
    messages.success(request, "Your account have been deleted!")
    return redirect('accounts:home')

class FTFDashboardView(TeacherTestMixin, TemplateView):
    template_name = "ftf/ftf_dashboard.html"

def ftf_addStudent(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = FTF_Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('teachers:ftf_dashboard')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('teachers:ftf_dashboard')

    context = {'studentForm':studentForm}
    return render(request, 'ftf/ftf_addstudent.html', context)

class FTFSearchStudentView(TeacherTestMixin, TemplateView):
    template_name = "ftf/ftf_searchstudent.html"

def ftf_searchStudent(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            course = request.POST['course']
            student = FTF_Student.objects.get(registration_id = reg_id, course = course)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return render(request, 'ftf/ftf_searchstudent.html')
            #return redirect('teachers:ftf/ftf_searchstudent')
    return render(request, 'ftf/ftf_studentprofile.html', context)

def ftf_updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = FTF_Student.objects.get(registration_id = request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(data = request.POST, files=request.FILES, instance = student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('teachers:ftf_searchStudent')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('teachers:ftf_searchStudent')
    return render(request, 'ftf/ftf_studentprofile.html', context)

class FTFTakeAttendanceView(TeacherTestMixin, TemplateView):
    template_name = "ftf/ftf_attendance.html"

def ftf_takeAttendance(request):
    if request.method == 'POST':
        details = {
            'course':request.POST['course'],
            'year': request.POST['year'],
            'block':request.POST['block'],
            'subject':request.POST['subject'],
            'period':request.POST['period'],
            'faculty':request.user.username
            }
        if FTF_Attendance.objects.filter(date = str(date.today()),course = details['course'], year = details['year'], block = details['block'], period = details['period'], subject = details['subject']).count() != 0 :
            messages.error(request, "Attendance already recorded.")
            return render(request, 'ftf/ftf_attendance.html')
            #return redirect('ftf:ftf_attendance')
        else:
            students = FTF_Student.objects.filter(course = details['course'], year = details['year'], block = details['block'])
            names = Recognizer2(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendance = FTF_Attendance(Faculty_Name = request.user.username, 
                    Student_ID = str(student.registration_id), 
                    period = details['period'], 
                    course = details['course'], 
                    year = details['year'], 
                    block = details['block'],
                    subject = details['subject'],
                    status = 'Present')
                    attendance.save()
                else:
                    attendance = FTF_Attendance(Faculty_Name = request.user.username, 
                    Student_ID = str(student.registration_id), 
                    period = details['period'],
                    course = details['course'],
                    subject = details['subject'],
                    year = details['year'], 
                    block = details['block'])
                    attendance.save()
            attendances = FTF_Attendance.objects.filter(date = str(date.today()), course = details['course'], year = details['year'], block = details['block'],period = details['period'])
            context = {"attendances":attendances, "ta":True}
            messages.success(request, "Attendance taking Success")
            return render(request, 'ftf/ftf_attendancelist.html', context)        
    context = {}
    return render(request, 'attendance/ftf_attendance.html', context)

class FTFAttendanceListView(TeacherTestMixin, TemplateView):
    template_name = "ftf/ftf_attendancelist.html"

def ftf_searchAttendance(request):
    attendances = FTF_Attendance.objects.all()
    myFilter = AttendanceFilter2(request.GET, queryset=attendances)
    attendances = myFilter.qs
    context = {'myFilter':myFilter, 'attendances': attendances, 'ta':False}
    return render(request, 'ftf/ftf_attendancelist.html', context)

def ftf_deleteAtt(request, id):
    attendance = FTF_Attendance.objects.get(pk=id)
    attendance.delete()
    messages.success(request, "Attendance deleted.")
    return redirect('teachers:ftf_dashboard')