from django.urls import include, path
from .views import (DashboardView,
                    ClassroomDetailView,
                    ProfileView,
                    edit_profile,
                    edit_profile_email,
                    edit_profile_info,
                    edit_profile_id,
                    edit_profile_passw,
                    change_photo,
                    attendance,
                    attendance_record,
                    delete_attendance,
                    joinClassroomView,
                    LeaveClassroomView,
                    deleting,
                    delete_acc 
                    )

app_name = 'students'

urlpatterns = [
    path('',                                DashboardView.as_view(),      name='dashboard'),
    path('profile/',                        ProfileView.as_view(),        name='profile'),
    path('edit_profile/',                   edit_profile,                 name='edit_profile'),
    path('edit_profile_email/',             edit_profile_email,           name='edit_profile_email'),
    path('edit_profile_id/',                edit_profile_id,              name='edit_profile_id'),
    path('edit_profile_info/',              edit_profile_info,            name='edit_profile_info'),
    path('edit_profile_passw/',             edit_profile_passw,           name='edit_profile_passw'),
    path('classroom/<slug:code>/',          ClassroomDetailView,          name='classroom_detail'),
    path('attendance/',                     attendance,                   name='attendance'),
    path('student_profile/',                change_photo,                 name='student_profile'),
    path('delete_attendance/<int:id>/',     delete_attendance,            name='delete_attendance'),
    path('attendance_record/<slug:code>/',  attendance_record,            name='attendance_record'),
    path('join-new/',                       joinClassroomView,            name='join_classroom'),
    path('leave-classroom/<slug:code>/',    LeaveClassroomView,           name='leave_classroom'),
    path('deleting/',                       deleting,                     name='deleting'),
    path('delete_acc/<int:id>/',            delete_acc,                   name='delete_acc')
]
