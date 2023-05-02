import django_filters

from accounts.models import Attendance, FTF_Attendance

class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['student_name','status','time', 'sub', 'grade/year']

class AttendanceFilter2(django_filters.FilterSet):
    class Meta:
        model = FTF_Attendance
        fields = '__all__'
        exclude = ['Faculty_Name', 'status','time','course','block']