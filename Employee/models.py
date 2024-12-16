from django.db import models

# Create your models here.

class Empdata(models.Model):
    
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    mon = models.CharField(db_column='mon', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tue = models.CharField(db_column='tue', max_length=150, blank=True, null=True)  # Field name made lowercase.
    wed = models.CharField(db_column='wed', max_length=150, blank=True, null=True)  # Field name made lowercase.
    thu = models.CharField(db_column='thu', max_length=150, blank=True, null=True)  # Field name made lowercase.
    fri = models.CharField(db_column='fri', max_length=150, blank=True, null=True)  # Field name made lowercase.
    sat = models.CharField(db_column='sat', max_length=150, blank=True, null=True)  # Field name made lowercase.
    sun = models.CharField(db_column='sun', max_length=150, blank=True, null=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=150, blank=True, null=True)
    status = models.CharField(db_column='status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    start = models.CharField(db_column='start', max_length=150, blank=True, null=True)  # Field name made lowercase.
    end = models.CharField(db_column='[end]', max_length=150, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='total', max_length=150, blank=True, null=True)  # Field name made lowercase.
    totals = models.CharField(db_column='week_total', max_length=150, blank=True, null=True)  # Field name made lowercase.
    statushr = models.CharField(db_column='status_hr', max_length=150, blank=True, null=True)  # Field name made lowercase.
    date_created = models.CharField(db_column='date_created', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='manager_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='hr_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    assigned = models.CharField(db_column='assigned', max_length=150, blank=True, null=True)  # Field name made lowercase.
    work_location = models.CharField(db_column='work_location', max_length=150, blank=True, null=True)  # Field name made lowercase.
    office_manager = models.CharField(db_column='office_manager', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status_om = models.CharField(db_column='status_om', max_length=150, blank=True, null=True)  # Field name made lowercase.

    
    class Meta:
        managed = True
        db_table = 'empdata'
        
class EmpLeaves(models.Model):
    
    emp_id = models.CharField(db_column='EMP_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    leave_type = models.CharField(db_column='LEAVE_TYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    from_dt = models.CharField(db_column='FROM', max_length=150, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    to_dt = models.CharField(db_column='TO', max_length=150, blank=True, null=True)  # Field name made lowercase.
    day_type = models.CharField(db_column='DAY_TYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    no_of_days = models.CharField(db_column='NO_OF_DAYS', max_length=150, blank=True, null=True)  # Field name made lowercase.
    remaining_leaves = models.CharField(db_column='REMAINING_LEAVES', max_length=150, blank=True, null=True)  # Field name made lowercase.
    leave_taken = models.CharField(db_column='LEAVE_TAKEN', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='reason', max_length=350, blank=True, null=True)  # Field name made lowercase.
    date_applied = models.CharField(db_column='date_applied', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='user_type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    valid_leaves = models.CharField(db_column='valid_leaves', max_length=150, blank=True, null=True)  # Field name made lowercase.
    paid_leaves = models.CharField(db_column='paid_leaves', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hr_id = models.CharField(db_column='hr_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='manager_id', max_length=150, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'EMP_LEAVES'

class Activities(models.Model):    
    emp_id = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=150, blank=True, null=True)
    currentdate = models.CharField(db_column='currentDate', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activities'




        