from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path('Emp_dashboard',views.home),
    path('Emp_EditProfile',views.Emp_EditProfile),
    path('Emp_tracker',views.Emp_tracker),

    path('Emp_leave',views.Emp_leave),
    path('mon_data',views.mon_data),
    path('tue_data',views.tue_data),
    path('wed_data',views.wed_data),
    path('thu_data',views.thu_data),
    path('fri_data',views.fri_data),
    path('sat_data',views.sat_data),
    path('Emp_notification',views.Emp_notification),
    path('Emp_profile',views.Emp_profile),
    path('Emp_report',views.Emp_report),
    path('Emp_Project_List',views.Emp_Project_List),
    path('Emp_Project_task',views.Emp_Project_task),


]


