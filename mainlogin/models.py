from django.db import models
import datetime
import os
# Create your models here.
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('static/uploads/', filename)

class Login(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
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
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    passwordstatus  = models.CharField(db_column='passwordchange', max_length=100, blank=True, null=True)  # Field name made lowercase.
    activation = models.CharField(db_column='activation', max_length=100, blank=True, null=True)  
    work_location = models.CharField(db_column='work_location', max_length=100, blank=True, null=True)  
    office_manager = models.CharField(db_column='office_manager', max_length=100, blank=True, null=True)  
    
    class Meta:
        managed = True
        db_table = 'LOGIN'
class UserType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_type = models.CharField(db_column='USER_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USER_TYPE'