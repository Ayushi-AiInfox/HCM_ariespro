from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.dashboard),
    path('Admin_dashboard',views.dashboard),
    path('Admin_leave',views.admin_leave),
    path('Admin_projects',views.admin_projects),
    path('Admin_profile',views.admin_profile),
    path('Admin_EditProfile',views.admin_editProfile),
    path('Admin_user',views.admin_addUser),
    path('Admin_Employee_Details',views.admin_empDetails),
    path('Admin_timesheet',views.admin_timesheet),
    path('Admin_notification',views.Admin_notification),
    path('Admin_Edit_Hr',views.Admin_Edit_Hr),
    path('Admin_Edit_Manager',views.Admin_Edit_Manager),
    path('Admin_Project_task',views.Admin_Project_task),
    path('Admin_phase',views.Admin_phase),
    path('change_activation',views.change_activation),
    path('Admin_reset_password',views.reset_password),
    ]