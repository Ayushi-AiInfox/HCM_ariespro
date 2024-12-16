from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path('OM_dashboard',views.home),
    path('OM_approvedTimesheet',views.OM_approvedTimesheet),
    path('OM_EditProfile',views.OM_EditProfile),
    path('OM_pendingTimesheet',views.OM_pendingTimesheet),
    path('OM_notification',views.OM_notification),
    path('OM_profile',views.OM_profile),
    path('OM_empTracker',views.OM_empTracker),
    path('OM_empTracker_Details',views.OM_empTracker_Details),
    path('OM_leave',views.OM_leave),
    path('OM_team',views.OM_team),
    path('OM_projects',views.OM_projects),
    path('OM_Project_task',views.OM_Project_task),
    # path('task_chat',views.task_chat),
    # path('task_chat_refresh',views.task_chat_refresh),
    # path('status_change',views.status_change),
    # path('task_status_mark',views.task_status_mark),
    path('OM_Employee_Details',views.Admin_Employee_Details),
    path('OM_phase',views.OM_phase),
    # path('change_task_status',views.change_task_status),
    # path('change_task_crew',views.change_task_crew),

]