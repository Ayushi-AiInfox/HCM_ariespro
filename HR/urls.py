from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home),
    path('HR_dashboard',views.home),
    path('HR_approvedTimesheet',views.HR_approvedTimesheet),
    path('HR_EditProfile',views.HR_EditProfile),
    path('HR_teamReport',views.HR_teamReport),
    path('HR_notification',views.HR_notification),
    path('HR_empList',views.HR_empList),
    path('HR_leave',views.HR_leave),
    path('HR_profile',views.HR_profile),
    # path('HR_team',views.HR_team),
    # path('HR_projects',views.HR_projects),
    path('HR_pendingTimesheet',views.HR_pendingTimesheet),
    path('HR_empTracker',views.HR_empTracker),
    path('HR_empTracker_Details',views.HR_empTracker_Details),
    path('HR_editEmp',views.HR_editEmp),
    path('HR_Edit_Hr',views.HR_Edit_Hr),
    path('HR_Edit_Manager',views.HR_Edit_Manager),
    path('HR_attendance',views.HR_attendance),
    path('HR_payment_payroll',views.HR_payment_payroll),
    path('attendance_test',views.attendance_test),
    path('attendance_test_create',views.attendance_test_create),
    path('payroll',views.HR_payroll),
    path('leave_test',views.leave_test),
    path('filter/', views.filter_data),
    path('filter_add_emp/', views.filter_data_add_emp),
    path('payroll/<str:emp_name>', views.payroll_emp),
    ]