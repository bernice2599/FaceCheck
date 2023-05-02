from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, CreateView, ListView
from .forms import *
from accounts.passtests import StudentTestMixin, TeacherTestMixin
import face_recognition

# Create your views here.

class user_consent(TemplateView):
    template_name = "accounts/user_consent.html"

class HomeView(TemplateView):
    template_name = "accounts/home.html"

class IndexView(TemplateView):
    template_name = "accounts/index.html"

class StudentCreateView(CreateView):
    model = User
    form_class = StudentForm
    template_name = "accounts/student_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')


class TeacherCreateView(CreateView):
    model = User
    form_class = TeacherForm
    template_name = "accounts/teacher_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

    