# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DesignationMaster(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DESIGNATION_MASTER'


class EmpDesk(models.Model):
    login_id = models.IntegerField(db_column='LOGIN_ID', blank=True, null=True)  # Field name made lowercase.
    f_name = models.CharField(db_column='F_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    l_name = models.CharField(db_column='L_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.CharField(db_column='EMP_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='MANAGER_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='HR_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    employment = models.CharField(db_column='EMPLOYMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    doj = models.DateField(db_column='DOJ', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mobile_alt = models.CharField(db_column='MOBILE_ALT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    salary = models.CharField(db_column='SALARY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bank_name = models.CharField(db_column='BANK_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    account_number = models.CharField(db_column='ACCOUNT_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ifsc = models.CharField(db_column='IFSC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    branch = models.CharField(db_column='BRANCH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.CharField(db_column='CRT_DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    current_project = models.CharField(db_column='CURRENT_PROJECT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    team_name = models.CharField(db_column='TEAM_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    leave_taken = models.CharField(db_column='LEAVE_TAKEN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    leave_remaining = models.CharField(db_column='LEAVE_REMAINING', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designations = models.CharField(max_length=50, blank=True, null=True)
    managers = models.CharField(max_length=50, blank=True, null=True)
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    activation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMP_DESK'


class EmpLeaves(models.Model):
    id = models.AutoField()
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    leave_type = models.CharField(db_column='LEAVE_TYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    from_field = models.CharField(db_column='FROM', max_length=150, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    to = models.CharField(db_column='TO', max_length=150, blank=True, null=True)  # Field name made lowercase.
    day_type = models.CharField(db_column='DAY_TYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    no_of_days = models.CharField(db_column='NO_OF_DAYS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    remaining_leaves = models.CharField(db_column='REMAINING_LEAVES', max_length=150, blank=True, null=True)  # Field name made lowercase.
    leave_taken = models.CharField(db_column='LEAVE_TAKEN', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=150, blank=True, null=True)
    reason = models.CharField(max_length=2000, blank=True, null=True)
    date_applied = models.CharField(max_length=150, blank=True, null=True)
    user_type = models.CharField(max_length=150, blank=True, null=True)
    valid_leaves = models.CharField(max_length=150, blank=True, null=True)
    paid_leaves = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)
    manager_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMP_LEAVES'


class LeaveDetails(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    remaining = models.CharField(db_column='REMAINING', max_length=150, blank=True, null=True)  # Field name made lowercase.
    taken = models.CharField(db_column='TAKEN', max_length=150, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(max_length=250, blank=True, null=True)
    days_allowed = models.CharField(db_column='DAYS_ALLOWED', max_length=150, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    sick_day = models.CharField(db_column='SICK_DAY', max_length=150, blank=True, null=True)  # Field name made lowercase.
    work_from_home = models.CharField(db_column='WORK_FROM_HOME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='User_Type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    reset_date = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LEAVE_DETAILS'


class Login(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='User_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    f_name = models.CharField(db_column='F_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    l_name = models.CharField(db_column='L_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    profile_photo = models.CharField(db_column='PROFILE_PHOTO', max_length=250, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.DateTimeField(db_column='CRT_DATE', blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(blank=True, null=True)
    passwordchange = models.CharField(max_length=100, blank=True, null=True)
    activation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LOGIN'


class Managers(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='HR_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MANAGERS'


class ManagerDesk(models.Model):
    emp_name = models.CharField(db_column='EMP_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    date_field = models.DateField(db_column='DATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    total_hours = models.TimeField(db_column='TOTAL_HOURS', blank=True, null=True)  # Field name made lowercase.
    status_field = models.CharField(db_column='STATUS_', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'MANAGER_DESK'


class ProjectDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    client_name = models.CharField(db_column='CLIENT_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.IntegerField(db_column='MANAGER_ID', blank=True, null=True)  # Field name made lowercase.
    employee_id = models.IntegerField(db_column='EMPLOYEE_ID', blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='START_DATE', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='END_DATE', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.DateTimeField(db_column='CRT_DATE', blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='MANAGER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(db_column='TEAM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PROJECT_DETAILS'


class UserType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='USER_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_TYPE'


class Activities(models.Model):
    id = models.AutoField()
    emp_id = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=150, blank=True, null=True)
    currentdate = models.CharField(db_column='currentDate', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activities'


class Attendance(models.Model):
    id = models.AutoField()
    user = models.CharField(db_column='USER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='MONTH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='YEAR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day1 = models.CharField(db_column='DAY1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day2 = models.CharField(db_column='DAY2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day3 = models.CharField(db_column='DAY3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day4 = models.CharField(db_column='DAY4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day5 = models.CharField(db_column='DAY5', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day6 = models.CharField(db_column='DAY6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day7 = models.CharField(db_column='DAY7', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day8 = models.CharField(db_column='DAY8', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day9 = models.CharField(db_column='DAY9', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day10 = models.CharField(db_column='DAY10', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day11 = models.CharField(db_column='DAY11', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day12 = models.CharField(db_column='DAY12', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day13 = models.CharField(db_column='DAY13', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day14 = models.CharField(db_column='DAY14', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day15 = models.CharField(db_column='DAY15', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day16 = models.CharField(db_column='DAY16', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day17 = models.CharField(db_column='DAY17', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day18 = models.CharField(db_column='DAY18', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day19 = models.CharField(db_column='DAY19', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day20 = models.CharField(db_column='DAY20', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day21 = models.CharField(db_column='DAY21', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day22 = models.CharField(db_column='DAY22', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day23 = models.CharField(db_column='DAY23', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day24 = models.CharField(db_column='DAY24', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day25 = models.CharField(db_column='DAY25', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day26 = models.CharField(db_column='DAY26', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day27 = models.CharField(db_column='DAY27', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day28 = models.CharField(db_column='DAY28', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day29 = models.CharField(db_column='DAY29', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day30 = models.CharField(db_column='DAY30', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day31 = models.CharField(db_column='DAY31', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attendance'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empdata(models.Model):
    id = models.AutoField()
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    mon = models.CharField(max_length=150, blank=True, null=True)
    tue = models.CharField(max_length=150, blank=True, null=True)
    wed = models.CharField(max_length=150, blank=True, null=True)
    thu = models.CharField(max_length=150, blank=True, null=True)
    fri = models.CharField(max_length=150, blank=True, null=True)
    sat = models.CharField(max_length=150, blank=True, null=True)
    sun = models.CharField(max_length=150, blank=True, null=True)
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=150, blank=True, null=True)
    start = models.CharField(max_length=150, blank=True, null=True)
    end = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    total = models.CharField(max_length=150, blank=True, null=True)
    week_total = models.CharField(max_length=150, blank=True, null=True)
    status_hr = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.CharField(max_length=150, blank=True, null=True)
    manager_id = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empdata'


class Hrteam(models.Model):
    id = models.AutoField()
    emp_id = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    user_typ = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    project = models.CharField(max_length=150, blank=True, null=True)
    team = models.CharField(max_length=150, blank=True, null=True)
    manager = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrteam'


class Notifications(models.Model):
    id = models.AutoField()
    emp_id = models.CharField(max_length=150, blank=True, null=True)
    emp_name = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=150, blank=True, null=True)
    current_date = models.CharField(max_length=150, blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    hr = models.CharField(max_length=10, blank=True, null=True)
    manager = models.CharField(max_length=10, blank=True, null=True)
    emp = models.CharField(max_length=10, blank=True, null=True)
    hr_id = models.CharField(max_length=10, blank=True, null=True)
    manager_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Payroll(models.Model):
    id = models.AutoField()
    employee = models.CharField(db_column='Employee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salary_per_month = models.CharField(db_column='Salary_per_month', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paid_sick_leave = models.CharField(max_length=50, blank=True, null=True)
    paid_sick_leave_rs = models.CharField(max_length=50, blank=True, null=True)
    paid_holiday = models.CharField(max_length=50, blank=True, null=True)
    paid_holiday_rs = models.CharField(max_length=50, blank=True, null=True)
    paid_vacation_day = models.CharField(max_length=50, blank=True, null=True)
    paid_vacation_day_rs = models.CharField(max_length=50, blank=True, null=True)
    unpaid_vacation = models.CharField(max_length=50, blank=True, null=True)
    unpaid_vacation_rs = models.CharField(max_length=50, blank=True, null=True)
    internet_charges_rs = models.CharField(max_length=50, blank=True, null=True)
    salary_and_other_harges_rs = models.CharField(max_length=50, blank=True, null=True)
    paid_to_employee = models.CharField(max_length=50, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    month = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    paid = models.CharField(max_length=50, blank=True, null=True)
    hr_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payroll'


class ProjectTeam(models.Model):
    id = models.AutoField()
    project = models.CharField(max_length=150, blank=True, null=True)
    team = models.CharField(max_length=150, blank=True, null=True)
    manager = models.CharField(max_length=150, blank=True, null=True)
    employee_name = models.CharField(max_length=150, blank=True, null=True)
    employee_id = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    crt_date = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_team'


class Ratings(models.Model):
    emp_id = models.CharField(max_length=150, blank=True, null=True)
    rating = models.CharField(max_length=150, blank=True, null=True)
    startdate = models.CharField(max_length=150, blank=True, null=True)
    enddate = models.CharField(max_length=150, blank=True, null=True)
    comment = models.CharField(max_length=150, blank=True, null=True)
    createdate = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)
    manager_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'
