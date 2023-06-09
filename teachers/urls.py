from django.urls import include, path
from .views import (DashboardView, 
                    ClassroomCreateView, 
                    ClassroomDeleteView, 
                    attendance,
                    ProfileTeacherView,
                    edit_profile,
                    edit_profile_usern,
                    edit_profile_email,
                    edit_profile_info,
                    edit_profile_passw,
                    TakeAttendanceView,
                    delete_attendance,
                    toggle_status_on,
                    toggle_status_off,
                    ClassroomDetailView, 
                    ClassroomStudentsView, 
                    deleting,
                    delete_acc,
                    FTFDashboardView,
                    ftf_addStudent,
                    FTFSearchStudentView,
                    ftf_searchStudent,
                    ftf_updateStudent,
                    FTFTakeAttendanceView,
                    ftf_takeAttendance,
                    FTFAttendanceListView,
                    ftf_searchAttendance,
                    ftf_deleteAtt,
                )

app_name = 'teachers'

urlpatterns = [
    path('',                                DashboardView.as_view(),        name='dashboard'),
    path('teacherprofile/',                 ProfileTeacherView.as_view(),          name='teacherprofile'), 
    path('edit_profile/',                   edit_profile,                   name='edit_profile'),
    path('edit_profile_email/',             edit_profile_email,             name='edit_profile_email'),
    path('edit_profile_usern/',             edit_profile_usern,             name='edit_profile_usern'),
    path('edit_profile_info/',              edit_profile_info,              name='edit_profile_info'),
    path('edit_profile_passw/',             edit_profile_passw,             name='edit_profile_passw'),
    path('classroom/add/',                  ClassroomCreateView.as_view(),  name='add_classroom'),
    path('classroom/<slug:code>/delete/',   ClassroomDeleteView.as_view(),  name='delete_classroom'),
    path('take_attendance/<slug:code>/',    TakeAttendanceView,             name='take_attendance'),
    path('toggle_status_on/<int:id>/'   ,   toggle_status_on,               name='toggle_status_on'),
    path('toggle_status_off/<int:id>/'   ,  toggle_status_off,              name='toggle_status_off'),
    path('attendance/',                     attendance,                     name='attendance'),
    path('take_attendance/<slug:code>/',    TakeAttendanceView,             name='take_attendance'),
    path('delete_attendance/<int:id>/',     delete_attendance,              name='delete_attendance'),
    path('classroom/<slug:code>/',          ClassroomDetailView,            name='classroom_detail'),
    path('classroom/<slug:code>/students/', ClassroomStudentsView,          name='classroom_students'),
    path('deleting/',                       deleting,                       name='deleting'),
    path('delete_acc/<int:id>/',            delete_acc,                     name='delete_acc'),

    path('ftf_dashboard/',              FTFDashboardView.as_view(),             name= 'ftf_dashboard'),
    path('ftf_addStudent/',             ftf_addStudent,                         name= 'ftf_addstudent'),
    path('ftf_searchstudentview/',      FTFSearchStudentView.as_view(),         name= 'ftf_searchstudentview'),
    path('ftf_searchStudent/',          ftf_searchStudent,                      name= 'ftf_searchStudent'),
    path('ftf_updateStudent/',          ftf_updateStudent,                      name= 'ftf_updateStudent'),
    path('ftf_takeattendanceview/',     FTFTakeAttendanceView.as_view(),        name= 'ftf_takeattendanceview'),
    path('ftf_attendancelistview/',     FTFAttendanceListView.as_view(),        name= 'ftf_attendancelistview'),
    path('ftf_takeAttendance/',         ftf_takeAttendance,                     name='ftf_takeAttendance'),
    path('ftf_searchAttendance/',       ftf_searchAttendance,                   name='ftf_searchAttendance'),
    path('ftf_deleteAtt/<int:id>/',     ftf_deleteAtt,                          name='ftf_deleteAtt'),
]
