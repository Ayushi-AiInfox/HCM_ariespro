from django.db import models

class Notifications(models.Model):
    
    emp_id = models.CharField(db_column='emp_id',max_length=150, blank=True, null=True)
    emp_name = models.CharField(db_column='emp_name',max_length=150, blank=True, null=True)
    message = models.TextField(db_column='message',blank=True, null=True)
    date = models.CharField(max_length=150, blank=True, null=True)
    current_date = models.CharField(max_length=150, blank=True, null=True)
    emp = models.CharField(db_column='emp', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hr = models.CharField(db_column='hr', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='manager', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='manager_id', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='hr_id', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'notifications'

class Ratings(models.Model):
    emp_id = models.CharField(max_length=150, blank=True, null=True)
    rating = models.CharField(max_length=150, blank=True, null=True)
    startdate = models.CharField(max_length=150, blank=True, null=True)
    enddate = models.CharField(max_length=150, blank=True, null=True)
    createdate = models.CharField(max_length=150, blank=True, null=True)
    hr_id = models.CharField(max_length=150, blank=True, null=True)
    manager_id = models.CharField(max_length=150, blank=True, null=True)
    manager_comment = models.CharField(max_length=1000, blank=True, null=True)
    employee_comment = models.CharField(max_length=1000, blank=True, null=True)
    emp_comm_tue = models.CharField(max_length=1000, blank=True, null=True)
    emp_comm_wed = models.CharField(max_length=1000, blank=True, null=True)
    emp_comm_thu = models.CharField(max_length=1000, blank=True, null=True)
    emp_comm_fri = models.CharField(max_length=1000, blank=True, null=True)
    emp_comm_sat = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'ratings'

class Tasks(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    project_id = models.CharField(db_column='PROJECT_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    team_id = models.CharField(db_column='TEAM_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, null=True)
    assigning_date = models.CharField(db_column='ASSIGNING_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    target_date = models.CharField(db_column='TARGET_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    complete_date = models.CharField(db_column='COMPLTE_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='MANAGER_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='HR_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.CharField(db_column='CRT_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ui = models.CharField(db_column='UI', max_length=150, blank=True, null=True)  # Field name made lowercase.
    database = models.CharField(db_column='DATABASE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    backend = models.CharField(db_column='BACKEND', max_length=150, blank=True, null=True)  # Field name made lowercase.
    projec_task_id = models.CharField(db_column='PROJEC_TASK_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(db_column='PHASE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    project_version = models.CharField(db_column='PROJECT_VERSION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    task_heading = models.CharField(db_column='TASK_HEADING', max_length=150, blank=True, null=True)  # Field name made lowercase.
    task_type = models.CharField(db_column='TASK_TYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='PRIORITY', max_length=150, blank=True, null=True)  # Field name made lowercase.
    assignee = models.CharField(db_column='ASSIGNEE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TASKS'

class TasksChats(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    task_id = models.CharField(db_column='TASK_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    team_id = models.CharField(db_column='TEAM_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.CharField(db_column='CRT_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TASKS_CHATS'

class TasksLogs(models.Model):
    # id = models.AutoField(db_column='ID')  # Fsield name made lowercase.
    project_id = models.CharField(db_column='PROJECT_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    task_id = models.CharField(db_column='TASK_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    from_status = models.CharField(db_column='FROM_STATUS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    to_status = models.CharField(db_column='TO_STATUS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    assigning_date = models.CharField(db_column='ASSIGNING_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    target_date = models.CharField(db_column='TARGET_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    complte_date = models.CharField(db_column='COMPLTE_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='MANAGER_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    crt_date = models.CharField(db_column='CRT_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TASKS_LOGS'

class TaskCrew(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    task_id = models.CharField(db_column='TASK_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    employee_name = models.CharField(db_column='EMPLOYEE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status =  models.CharField(db_column='STATUS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TASK_CREW'

class PhaseVersion(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=150, blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(db_column='PHASE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    start_date = models.CharField(db_column='START_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    time_period = models.CharField(db_column='TIME_PERIOD', max_length=150, blank=True, null=True)  # Field name made lowercase.
    end_date = models.CharField(db_column='END_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PHASE_VERSION'

class TaskFiles(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    task_id = models.CharField(db_column='TASK_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    file_name = models.CharField(db_column='FILE_NAME', max_length=250, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATEtime', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TASK_FILES'

class Versions(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    project = models.CharField(db_column='project', max_length=150, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='version', max_length=150, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='create_date', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VERSIONS'




 