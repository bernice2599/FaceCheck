from urllib import response
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django import views
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, View
from accounts.models import *
from accounts.passtests import StudentTestMixin, TeacherTestMixin
from .forms import JoinClassroomForm, AttendanceForm, PhotoForm
from .filters import AttendanceFilter
from .recognizer import Recognizer
from django.contrib import messages
from datetime import date
import datetime
import xlwt
import os
from accounts.forms import StudentForm

# Create your views here.

class ProfileView(StudentTestMixin, TemplateView):
    template_name = "students/profile.html"

def edit_profile(request):
    return render(request,"students/edit_profile.html")

def edit_profile_info(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('students:edit_profile'))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")

        try:
            customuser=User.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.save()
            messages.success(request, "Profile updated.")
            return HttpResponseRedirect(reverse('students:profile'))
        except:
            return HttpResponseRedirect(reverse('students:edit_profile'))

def edit_profile_id(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('students:edit_profile'))
    else:
        student_id=request.POST.get("student_id")

        try:
            student=Student.objects.get(student_id=request.user.students.student_id)
            student.student_id = student_id
            # Student id validation
            if Student.objects.filter(student_id=student_id).exists():
                messages.error(request,"Student ID already exist.")
                return HttpResponseRedirect(reverse('students:edit_profile'))
            else:
                student.save()
                messages.success(request, "Student ID updated.")
                return HttpResponseRedirect(reverse('students:profile'))
        except:
            messages.error(request, "Failed to update.")
            return HttpResponseRedirect(reverse('students:edit_profile'))

def edit_profile_email(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('students:edit_profile'))
    else:
        email=request.POST.get("email")
        
        try:
            customuser=User.objects.get(id=request.user.id)
            customuser.email=email
            #Username Validations
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists.")
                return HttpResponseRedirect(reverse('students:edit_profile'))
            else:
                customuser.save()
                messages.success(request, "Email updated.")
                return HttpResponseRedirect(reverse('students:profile'))
        except:
            messages.error(request,"Failed to update.")
            return HttpResponseRedirect(reverse('students:edit_profile'))

def edit_profile_passw(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse('students:edit_profile'))
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
            return HttpResponseRedirect(reverse('students:edit_profile'))
        
def change_photo(request):
    if request.method=="POST":
        form=PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            img_path=request.user.students.picture.path
            if os.path.exists(img_path):
                os.remove(img_path)
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('students:student_profile')
    else:
        form=PhotoForm()
    return render(request,'students/student_profile.html',{'form':form})


class DashboardView(StudentTestMixin, TemplateView):
    template_name = "students/dashboard.html"

def ClassroomDetailView(request,code):
    context_dict = {}
    room = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = room
    return render(request, 'students/classroom_detail.html', context=context_dict)
   
def attendance(request):
    if request.method == 'POST':
        details = {
            'student_name':request.user.username,
            'student_no':request.user.students.student_id,
            'course':request.POST['course'],
            'grade_year':request.POST['grade_year'],
            'block_section':request.POST['block_section'],
            'sub':request.POST['sub'],
            }
        if Attendance.objects.filter(student_name = request.user.username, date = str(date.today()), course = details['course'], grade_year = details['grade_year'], block_section = details['block_section'], sub = details['sub']).count() != 0 :
            messages.error(request, "Attendance already recorded.")
            return redirect(reverse_lazy('students:classroom_detail'))
        else:
            names = Recognizer(details)
            if request.user.is_student:
                if request.user.username in names:
                    attendance = Attendance(student_name = request.user.username,
                    student_no = request.user.students.student_id,
                    course =  details['course'],
                    grade_year = details['grade_year'], 
                    block_section = details['block_section'],
                    sub = details['sub'],
                    status = 'Present')
                    attendance.save()
                else:
                    attendance = Attendance(student_name = request.user.username,
                    student_no = request.user.students.student_id,
                    course =  details['course'],
                    grade_year = details['grade_year'], 
                    block_section = details['block_section'],
                    sub = details['sub'])
                    attendance.save()
            attendances = Attendance.objects.filter(date = str(date.today()), student_no = request.user.students.student_id, course = details['course'], grade_year = details['grade_year'], block_section = details['block_section'], sub = details['sub'])
            context = {"attendances":attendances, "ta":True}
            messages.success(request, "Attendance taking Successful.")
            return render(request, 'students/attendance_done.html', context)        
    context = {}
    return render(request, 'students/dashboard.html', context)


def attendance_record(request,code):
    context_dict={}
    room = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = room
    attendances = Attendance.objects.all().order_by('date')
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    context_dict['myFilter'] = AttendanceFilter(request.GET, queryset=attendances)
    context_dict['attendances'] = myFilter.qs
    return render(request, 'students/attendance_record.html', context=context_dict,)


def delete_attendance(request, id):
    attendance = Attendance.objects.get(pk=id)
    attendance.delete()
    messages.success(request, "Attendance deleted.")
    return redirect('students:dashboard')

def joinClassroomView(request):
    form = JoinClassroomForm()
    
    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data['code']
            print(code)
            if Classroom.objects.filter(code=code).exists():
                print('Exists', form.cleaned_data['code'])
                
                if request.user.students.classrooms.filter(code=code).exists():
                    messages.error(request, "User already a member")
                    return HttpResponseRedirect(reverse('students:dashboard'))
                else:
                    print('User not a member')
                    request.user.students.classrooms.add(Classroom.objects.filter(code=code).first())
                    messages.success(request, "User joined the classroom")
                    return HttpResponseRedirect(reverse('students:dashboard')) 
            else:
                messages.error(request, "Classroom dosen't exist.")
    return render(request, 'students/join_classroom.html', {'form':form})

def LeaveClassroomView(request,code):
    request.user.students.classrooms.remove(Classroom.objects.filter(code=code).first())
    return HttpResponseRedirect(reverse('students:dashboard'))

def deleting(request):
    return render(request,'students/delete_acc.html')
    
def delete_acc(request, id):
    user = User.objects.get(pk=id)
    if len(user.students.picture) > 0:
        os.remove(user.students.picture.path)
    user.delete()
    messages.success(request, "Your account have been deleted!")
    return redirect('accounts:home')






