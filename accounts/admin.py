from django.contrib import admin

from .models import (
                    Attendance,
                    User,
                    Teacher,
                    Classroom,
                    Student,         
                )
# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Attendance)

