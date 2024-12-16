from django.db import models

# Create your models here.

class HrDesk(models.Model):
    emp_name = models.CharField(db_column='EMP_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    date_field = models.DateField(db_column='DATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    total_hours = models.CharField(db_column='TOTAL_HOURS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HR_DESK'
class LeaveDetails(models.Model):
    
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    remaining = models.CharField(db_column='REMAINING', max_length=150, blank=True, null=True)  # Field name made lowercase.
    taken = models.CharField(db_column='TAKEN', max_length=150, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='note', max_length=250, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    sick_day = models.CharField(db_column='SICK_DAY', max_length=150, blank=True, null=True)  # Field name made lowercase.
    work_from_home = models.CharField(db_column='WORK_FROM_HOME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    days_allowed = models.CharField(db_column='DAYS_ALLOWED', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='User_Type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    reset_date = models.CharField(db_column='reset_date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='hr_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
   

    class Meta:
        managed = True
        db_table = 'LEAVE_DETAILS'
        
class hrteam (models.Model):
    
    emp_id = models.CharField(db_column='emp_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='project', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_typ = models.CharField(db_column='user_type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(db_column='team', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='manager', max_length=150, blank=True, null=True)  # Field name made lowercase.
   
    
    
    

    
    class Meta:
        managed = True
        db_table = 'hrteam'

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
    hr_id = models.CharField(db_column='hr_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'PROJECT_DETAILS'

class Manager(models.Model):
    # Field name made lowercase.
    emp_id = models.CharField(db_column='emp_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='HR_ID', max_length=150, blank=True, null=True)
    client = models.CharField(db_column='CLIENT', max_length=150, blank=True, null=True)
    office_manager = models.CharField(db_column='OFFICE_MANAGER', max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'MANAGERS'

class Project_team(models.Model):
    
    project = models.CharField(db_column='project', max_length=150, blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(db_column='team', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='manager', max_length=150, blank=True, null=True)  # Field name made lowercase.
    employee_name = models.CharField(db_column='employee_name', max_length=250, blank=True, null=True)  # Field name made lowercase.
    employee_id = models.CharField(db_column='employee_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='designation', max_length=150, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.CharField(db_column='crt_date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='hr_id', max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'project_team'

class EmpDesk(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
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
    address = models.CharField(db_column='ADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
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
    activation = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'EMP_DESK'

class DesignationMaster(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DESIGNATION_MASTER'

class Attendance(models.Model):
    # id = models.AutoField()
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
    hr_id = models.CharField(db_column='hr_id', max_length=50, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'attendance'

class Payroll(models.Model):
    # id = models.AutoField()
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
    salary_and_other_charges_rs = models.CharField(db_column='salary_and_other_harges_rs', max_length=50, blank=True, null=True)
    paid_to_employee = models.CharField(max_length=50, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    month = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    paid = models.CharField(max_length=50, blank=True, null=True)
    hr_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'payroll'
