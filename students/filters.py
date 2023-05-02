import django_filters

from accounts.models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['student_name', 'student_no','status','grade_year', 'sub', 'block_section']
