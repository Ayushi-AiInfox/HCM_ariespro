from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path('CM_dashboard',views.home),
    path('CM_approvedTimesheet',views.CM_approvedTimesheet),
    path('CM_EditProfile',views.CM_EditProfile),
    path('CM_pendingTimesheet',views.CM_pendingTimesheet),
    path('CM_notification',views.CM_notification),
    path('CM_profile',views.CM_profile),
    path('CM_empTracker',views.CM_empTracker),
    path('CM_empTracker_Details',views.CM_empTracker_Details),
    path('CM_leave',views.CM_leave),
    path('CM_team',views.CM_team),
    path('CM_projects',views.CM_projects),
    path('CM_Project_task',views.CM_Project_task),
    path('task_chat',views.task_chat),
    path('task_chat_refresh',views.task_chat_refresh),
    path('status_change',views.status_change),
    path('task_status_mark',views.task_status_mark),
    path('CM_Employee_Details',views.Admin_Employee_Details),
    path('CM_phase',views.CM_phase),
    path('change_task_status',views.change_task_status),
    path('change_task_crew',views.change_task_crew),

]