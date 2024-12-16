from django.contrib import admin
from HR.models import  Attendance,ProjectDetails,Manager,Project_team,EmpDesk,LeaveDetails,DesignationMaster,Payroll
# Register your models here.
admin.site.register(Attendance),
admin.site.register(ProjectDetails),
admin.site.register(Manager),
admin.site.register(Project_team),
admin.site.register(EmpDesk),
admin.site.register(LeaveDetails),
admin.site.register(DesignationMaster),
admin.site.register(Payroll),



