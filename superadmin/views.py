from django.shortcuts import render, redirect
from HR.models import Attendance,Payroll,LeaveDetails,EmpDesk,ProjectDetails,Manager,Project_team,DesignationMaster
from datetime import datetime,date,timedelta
from django.http import HttpResponseRedirect
from Employee.models import Empdata,EmpLeaves
from django.db.models import Max
from django.db.models import F, Value
from django.db.models import CharField
from django.db.models import Case, When, Value
from django.db import connection
from ClientManager.models import Ratings,Notifications
from ClientManager.models import Tasks,TasksChats,TasksLogs
from django.db.models import DateField, CharField,IntegerField,Subquery, OuterRef
from ClientManager.models import Notifications,Tasks,TasksChats,TasksLogs,TaskCrew ,PhaseVersion,TaskFiles,Versions
from django.db.models import Count
from django.db.models import DateField, CharField,IntegerField,FloatField,Subquery, OuterRef
from django.db.models.functions import Cast
from django.db.models import Q
from cryptography.fernet import Fernet
from mainlogin.models import Login
import smtplib
from email.message import EmailMessage
import ssl
from django.http import JsonResponse
from cryptography.fernet import Fernet

# Create your views here.

def dashboard(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for login '
        response=HttpResponseRedirect('../../')
        return response

    if request.method=='GET':
        chart_year=date.today().year
        request.session['chart_year'] =str(chart_year)

    # chart_year=int(chart_year)

    if request.method=='POST':
        if 'emp_details' in request.POST:
            request.session['emp_details']=request.POST.get('emp_details')
            return redirect('../superadmin/Admin_Employee_Details')
        elif 'next' in request.POST:
            chart_year=request.session['chart_year']
            chart_year=int(chart_year)
            chart_year=chart_year+1
            request.session['chart_year'] =str(chart_year)
        elif 'prev' in request.POST:
            chart_year=request.session['chart_year']
            chart_year=int(chart_year)
            chart_year=chart_year-1
            request.session['chart_year'] =str(chart_year)
        elif 'reset' in request.POST:
            emp_id=request.POST.get('reset')
            request.session['reset_pwd']=emp_id
            return redirect('../superadmin/Admin_reset_password')
            

    x=datetime.now().date()
    y=datetime.now().date()
    for i in range(8):
        if x.weekday()==0:
            start=x
        else:
            x=x- timedelta(days=1, hours=0)
        if y.weekday()==6:
            end_dt=y
        else:
            y=y - timedelta(days=1, hours=0)
    
    end_dt=start+timedelta(days=6)
    request.session['start_date']=str(start)
    request.session['end_date']=str(end_dt)

    Project_teams=Project_team.objects.all().order_by('team')
    Emp_Desk=EmpDesk.objects.filter(emp_type='3')
    ratings=Ratings.objects.all()
    
    cursor=connection.cursor()
    cursor.execute(r"get_performance  'Poor'")
    poor=dictfetchall (cursor)
    print(poor,'poor----------------->>')
    cursor.execute(r"get_performance  'Top'")
    top=dictfetchall (cursor)
    cursor.execute(r"get_performance  'avg'")
    average=dictfetchall (cursor)
    cursor.execute(r"get_performance  'Performance'")
    performance=dictfetchall (cursor)
    # print(performance)
    print(average)
    try:

        average= round(average[0]['average'], 2)
        
        print(average,'---')
        average_maped=map_value(average)
        average=round(average*10,2)

    except:
        average_maped=0
        average=0

    data=EmpDesk.objects.filter(activation='Active').exclude(emp_type__in=['1','2'])
    print(data,'data')
    month1=[]
    month2=[]
    month3=[]
    month4=[]
    month5=[]
    month6=[]
    month7=[]
    month8=[]
    month9=[]
    month10=[]
    month11=[]
    month12=[]
    employees=[]
    for i in data:
        employees.append(i.f_name+' '+i.l_name)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=1,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)
        month1.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=2,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)            
        month2.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=3,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month3.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=4,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month4.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=5,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month5.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=6,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month6.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=7,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month7.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=8,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month8.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=9,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)        
        month9.append(hours) 
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=10,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)       
        month10.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=11,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)            
        month11.append(hours)
        hours=Empdata.objects.annotate(start_datetime=Cast('start', DateField())).filter(emp_id=i.login_id,start_datetime__month=12,start_datetime__year=chart_year,statushr='2')
        hours=[int(x.total) for x in hours]
        hours=sum(hours)    
        month12.append(hours)             
    print(len(employees),'employees',len(month1),'-month1', len(month2),'-month2', len(month3),'-month3', len(month4),'-month4', len(month5),'-month5', len(month6),'-month6', len(month7),'-month7', len(month8),'-month8', len(month9),'-month9', len(month10),'-month10', len(month11),'-month11', len(month12),'-month12', )    
    

    
    return render(request, 'Admin_dashboard.html',{'chart_year':chart_year, 'employees':employees,'month1':month1, 'month2':month2, 'month3':month3, 'month4':month4, 'month5':month5,
    'month6':month6, 'month7':month7, 'month8':month8, 'month9':month9, 'month10':month10, 'month11':month11, 'month12':month12,    'average_maped':average_maped,'Project_team':Project_teams,'EmpDesk':Emp_Desk ,'poor':poor ,'top':top ,'average':average ,'performance':performance})

def map_value(variable, min_variable=0, max_variable=10, min_mapped_value=0, max_mapped_value=100):
    mapped_value = ((variable - min_variable) / (max_variable - min_variable)) * (max_mapped_value - min_mapped_value) + min_mapped_value
    return mapped_value

def dictfetchall (cursor):
        columns = [col [0] for col in cursor.description]
        return [dict (zip (columns, row)) for row in cursor.fetchall ()]

def admin_leave(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="4":
        # manager_id = EmpDesk.objects.get(id=request.session['id']).manager_id
        name=request.session['name']
        sl=[]
        pl=[]
        leaves_detail=EmpLeaves.objects.filter(user_type='1').order_by('-id')
        for i in leaves_detail:
            detail=LeaveDetails.objects.filter(emp_id=i.emp_id)
            sl.append(detail[0].sick_day)
            pl.append(detail[0].days_allowed)
            print(i,detail[0].sick_day,detail[0].days_allowed)
        leaves=zip(sl,pl,leaves_detail)
        start_date,end_date=weekdates()
        #Manager
        sl=[]
        pl=[]
        leaves_detail=EmpLeaves.objects.filter(user_type='2').order_by('-id')
        for i in leaves_detail:
            detail=LeaveDetails.objects.filter(emp_id=i.emp_id)
            print(i.emp_id,'i.emp_id')
            sl.append(detail[0].sick_day)
            pl.append(detail[0].days_allowed)
        manager_leaves=zip(sl,pl,leaves_detail)

        #Employee
        sl=[]
        pl=[]
        leaves_detail=EmpLeaves.objects.filter(user_type='3').order_by('-id')
        for i in leaves_detail:
            detail=LeaveDetails.objects.filter(emp_id=i.emp_id)
            print('detail',i.emp_id)
            sl.append(detail[0].sick_day)
            pl.append(detail[0].days_allowed)
        employee_leaves=zip(sl,pl,leaves_detail)
        if 'approve' in request.POST:

                emp_id=int(request.POST.get('approve'))
                
                emp=EmpLeaves.objects.filter(id=emp_id)
                
                j=emp[0]
                leave_type=j.leave_type
                j.status = 'Approved'
                j.save(update_fields=['status'])
                
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your leave ({j.from_dt} - {j.to_dt}) is Approved ',date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
                mail_leave_start= j.from_dt
                mail_leave_end=j.to_dt
                emp_id=emp[0].emp_id
                typ=emp[0].day_type
                noofday=float(emp[0].no_of_days)
                
                leave_start=emp[0].from_dt
                leave_end=emp[0].to_dt
                leave_start= datetime.strptime(leave_start, '%Y-%m-%d')
                leave_end= datetime.strptime(leave_end, '%Y-%m-%d')
                
                leave_holiday=get_holiday_in_leaves(leave_start,leave_end)
                noofday=noofday-leave_holiday
             
                
                emp=LeaveDetails.objects.filter(emp_id=emp_id)
                i=emp[0]
                if leave_type=='Sick Leave':
                    if float(i.sick_day) <= 0:
                        i.sick_day=0
                        i.save(update_fields=['sick_day'])
                    else:
                    
                        sick_day=emp[0].sick_day
                        sick_day=float(sick_day)
                        new_sick_day=(float(sick_day)-noofday)
                        if new_sick_day<0:
                            new_sick_day=0
                        i.sick_day=new_sick_day
                        i.save(update_fields=['sick_day'])
                else:
                    try:
                        days_allowed=float(i.days_allowed)
                        
                    except:
                        days_allowed=0
                    if  days_allowed<= 0:
                        i.days_allowed=0
                        i.save(update_fields=['days_allowed'])
                    else:
                    
                        days_allowed=emp[0].days_allowed
                        days_allowed=float(days_allowed)
                        new_days_allowed=(float(days_allowed)-noofday)
                        if new_days_allowed<0:
                            new_days_allowed=0
                        i.days_allowed=new_days_allowed
                        i.save(update_fields=['days_allowed'])
                
                
                i.taken=(float(emp[0].taken)+noofday)
                i.save(update_fields=['taken'])

                remaning=i.remaining
                
                emp=EmpLeaves.objects.filter(emp_id=emp_id)

                j=emp[0]
                j.remaining_leaves = remaning
                j.save(update_fields=['remaining_leaves'])
                
                try:
                    leave = EmpDesk.objects.filter(login_id = emp_id)
                    l=leave[0]
                    
                    l.leave_taken = (float(leave[0].leave_taken) + noofday)
                    l.save(update_fields=['leave_taken'])
                    l.leave_remaining = (float(leave[0].leave_remaining) - noofday)
                    l.save(update_fields=['leave_remaining'])
                except:
                    pass

                # hr_mail=Login.objects.get(id=hr_id).email
                email=Login.objects.get(id=emp_id).email
                mail_name=Login.objects.get(id=request.session['id']).f_name
                l_name=Login.objects.get(id=request.session['id']).l_name
                mail_name=mail_name+' '+l_name
                sender = 'ats.ariespro@gmail.com'
                # receivers = email
                name_of_emp=Login.objects.get(id=emp_id).f_name
                receivers = email
                # receivers = 'karan.rana@ariespro.com'
                password = 'ahbfhcshjujvkgge'
                Subject= 'Leave Approved'
                
                message = f"""
                Hi {name_of_emp},   
                
                Your leave for ({mail_leave_start} to {mail_leave_end}) is Approved  by {mail_name} 
                
                To access the portal, please click on the following link: "https://hcm.ariespro.com/".

                Note: DO NOT REPLY TO THIS EMAIL. If you did not request this change, or if you believe you have 
                received this email in error, please email at it.support@ariespro.com.

                Thank you,
                AriesPro Utilities
                
                """

                server=EmailMessage()

                server['From']='Ariespro'
                server['To']=receivers
                server['Subject']=Subject
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    # with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    #     smtp.login(sender,password)
                    #     smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass
        elif 'reject' in request.POST:
                emp_id=int(request.POST.get('reject'))
                print(emp_id)
                
                emp=EmpLeaves.objects.filter(id=emp_id)
                
                i=emp[0]
                i.status='Rejected'
                i.save(update_fields=['status'])

                manage_attendance(request,i)
                j=emp[0]
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your leave ({j.from_dt} - {j.to_dt}) is Rejected',date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
                emp_id=j.emp_id

                #emp[0].note=request.POST.get('note')
                #emp[0].save(update_fields=['note'])
                
                email=Login.objects.get(id=emp_id).email
                mail_name=Login.objects.get(id=request.session['id']).f_name
                l_name=Login.objects.get(id=request.session['id']).l_name
                mail_name=mail_name+' '+l_name
                sender = 'ats.ariespro@gmail.com'
                # receivers = email
                name_of_emp=Login.objects.get(id=emp_id).f_name
                receivers = email
                # receivers = 'karan.rana@ariespro.com'
                password = 'ahbfhcshjujvkgge'
                Subject= 'Leave Rejected'
                
                message = f"""
                Hi {name_of_emp},   
                
                Your leave for ({j.from_dt} to {j.to_dt}) is Rejected  by {mail_name} 
                
                To access the portal, please click on the following link: "https://hcm.ariespro.com/".

                Note: DO NOT REPLY TO THIS EMAIL. If you did not request this change, or if you believe you have 
                received this email in error, please email at it.support@ariespro.com.

                Thank you,
                AriesPro Utilities
                
                """

                server=EmailMessage()

                server['From']='Ariespro'
                server['To']=receivers
                server['Subject']=Subject
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                try :
                    context=ssl.create_default_context()
                    # with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    #     smtp.login(sender,password)
                    #     smtp.sendmail(sender,receivers,server.as_string())
                except:
                    pass
            
        
        
        return render(request, 'Admin_leave.html', {'name1': name,'leaves_detail':leaves,'manager_leaves':manager_leaves, 'employee_leaves':employee_leaves})
    else:
        response=HttpResponseRedirect('../../')
        return response

    return render(request, 'Admin_leave.html')

def get_holiday_in_leaves(start_date,end_date):
    today = date.today()
    # start_date = date(today.year, today.month, 1)
    # end_date = start_date + timedelta(days=31) 
    # while end_date.month !=start_date.month:
    #     end_date=end_date - timedelta(days=1)
    print(start_date, end_date)
    sundays = []
    saturdays = []

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 6:  # Sunday is the 6th day of the week
            sundays.append(current_date)
        elif current_date.weekday() == 5:  # Saturday is the 5th day of the week
            saturdays.append(current_date)
        current_date += timedelta(days=1)
    
    first_saturday = None
    
    second_saturday = None
    third_saturday = None
    fourth_saturday = None
    fifth_saturday = None
    sat=[]
    for saturday in saturdays:
        if first_saturday is None:
            first_saturday = saturday
            
        elif second_saturday is None:
            second_saturday = saturday
            sat.append(saturday)
        elif third_saturday is None:
            third_saturday = saturday
            
        elif fourth_saturday is None:
            fourth_saturday = saturday
            sat.append(saturday)
        else:
            fifth_saturday = saturday
            sat.append(saturday)
    holiday=sundays+sat
    holiday=len(holiday)
    return holiday

def admin_projects(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="4":
        managers=Manager.objects.all()
        if request.method=='POST':
            if 'add'  in request.POST:
                date=request.POST.get('date')
                manager=request.POST.get('manager')
                client=request.POST.get('client')
                managerss=Manager.objects.get(emp_id=manager).name
                hr_id=Manager.objects.get(emp_id=manager).hr_id
                print('added')
                a=ProjectDetails(project_name=request.POST.get('project'),client_name=client,manager_id=manager,start_date=date,status='PENDING',manager=managerss,crt_date=datetime.now().date(),hr_id=hr_id)
                a.save()
            if 'edit' in request.POST:
                # project_id=request.POST.get('edit')
                # project=request.POST.get(f'project_edit{project_id}')
                # client=request.POST.get(f'client_edit{project_id}')
                # ProjectDetails.objects.filter(id=project_id).update(project_name=project,client_name=client)
                edit=request.POST.get('edit')
                project_edit=request.POST.get(f'project_edit{edit}')
                client_edit=request.POST.get(f'client_edit{edit}')
                Project_team.objects.filter(project=ProjectDetails.objects.filter(id = edit).first().project_name).update(project = project_edit)
                Tasks.objects.filter(project_id=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_id = project_edit)
                TasksLogs.objects.filter(project_id=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_id = project_edit)
                Empdata.objects.filter(project_name=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_name = project_edit)
                PhaseVersion.objects.filter(project=ProjectDetails.objects.filter(id = edit).first().project_name).update( project = project_edit) 
                ProjectDetails.objects.filter(id=edit).update( project_name= project_edit, client_name= client_edit)                                                  
                 
            elif 'project_name' in request.POST:
                request.session['project_name']=request.POST.get('project_name')
                response=HttpResponseRedirect('/superadmin/Admin_phase')
                return response    
            # name=request.session['name']
            # project=ProjectDetails.objects.filter(hr_id=request.session['id'])
            # return render(request,'CM_projects.html',{'name':name,'project':project,'managers':managers})

        project=ProjectDetails.objects.all()   
        name=request.session['name']
        return render(request,'Admin_projects.html',{'name':name,'project':project,'managers':managers})
    else:
        response=HttpResponseRedirect('../../')
        return response

    return render(request, 'Admin_projects.html')

def admin_profile(request):
    
    empl = Login.objects.filter(id=request.session['id'])
    empl = empl[0]
    
    return render(request, 'Admin_profile.html',{'profile':empl})

def admin_editProfile(request):
    # try:
        if request.session['user']=="4":

            message1 = ''
            message = ''
            empl = Login.objects.filter(id=request.session['id'])
            empl = empl[0]
            if request.method == 'POST':
                if 'editProfile' in request.POST:
                   
                    data = Login.objects.filter(id=request.session['id'])
                    data = data[0]
                    data.f_name=request.POST.get('fname')
                    data.save(update_fields=['f_name'])
                    data.l_name=request.POST.get('lname')
                    data.save(update_fields=['l_name'])
                    data.email=request.POST.get('email')
                    data.save(update_fields=['email'])
                    data.mobile=request.POST.get('mobileNo')
                    data.save(update_fields=['mobile'])
                    data.address=request.POST.get('addr')
                    data.save(update_fields=['address']) 
                    
                    # print(request.FILES,'hello world')
                    if len(request.FILES) != 0:
                        data.image = request.FILES['profile_pic']
                        data.save(update_fields=['image'])
                        task=Login.objects.filter(id=request.session['id'])
                        request.session['profile_pic']=str(task[0].image)
                    

                elif 'changePass' in request.POST:
                    data = Login.objects.filter(id=request.session['id'])
                    data = data[0]
                    pwd= data.password
                    try:
                        cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                        decryptedpassword = (cipher_suite.decrypt(pwd))
                        pwd=decryptedpassword.decode()
                    except:
                        pass
                    if data.password == request.POST.get('currPass'):
                        if request.POST.get('password') == request.POST.get('confirmPass'):
                            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                            cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                            ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                            # print(ciphered_text) 
                            pwd=ciphered_text.decode()
                            data.password=pwd
                            data.save(update_fields=['password'])

                        else:
                            message1 = 'password and confirm password must be same.'
                    elif pwd == request.POST.get('currPass'):
                        if request.POST.get('password') == request.POST.get('confirmPass'):
                            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                            cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                            ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                            # print(ciphered_text) 
                            pwd=ciphered_text.decode()
                            data.password=pwd
                            data.save(update_fields=['password'])

                        else:
                            message1 = 'password and confirm password must be same.'
                    
                    else:
                        message = 'current password is incorrect'

            name=request.session['name']
            empl = Login.objects.filter(id=request.session['id'])
            empl = empl[0]
            print(empl)
            return render(request, 'Admin_EditProfile.html',{'employee':empl})
        else:
            s='enter credentials for  login '
            response=HttpResponseRedirect('../../')
            return response

    # except:
    #     s='enter credentials for  login '
    #     response=HttpResponseRedirect('../../')
    #     return response

def admin_addUser(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if True:
        if 'add_mngr' in request.POST or 'add_hr' in request.POST :
            f_name=request.POST.get('fname')
            l_name=request.POST.get('lname')
            uname=request.POST.get('uname')
            pwd=request.POST.get('pwd')
            # encyption the password
            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
            cipher_suite = Fernet(key)
            ciphered_text = cipher_suite.encrypt(bytes(pwd ,encoding='utf8')) 
            pwd=ciphered_text.decode()
            mailid=request.POST.get('mailId')
            dob=request.POST.get('DOB')
            designation=request.POST.get('designation')
            gender=request.POST.get('gender')
            phoneNo=request.POST.get('phoneNo')
            AltPhoneNo=request.POST.get('AltPhoneNo')
            DOJ=request.POST.get('DOJ')
            salary=request.POST.get('salary')
            bankName=request.POST.get('bankName')
            acctNo=request.POST.get('acctNo')
            ifsc_code=request.POST.get('ifsc_code')
            branch=request.POST.get('branch')
            CurrProject=request.POST.get('CurrProject')
            try:
                CurrProject=ProjectDetails.objects.get(id=CurrProject).project_name
            except:
                pass
            teamName=request.POST.get('teamName')
            manager=request.POST.get('manager')
            hr_id=request.POST.get('HR')
            Address=request.POST.get('Address')
            try:
                manager_name=Manager.objects.get(emp_id=manager).name
            except:
                manager_name=''
            try:
                sivckLeaves=request.POST['sivckLeaves']
            except:
                sivckLeaves =0    
            try:
                otherleaves=request.POST['otherleaves']
            except:
                otherleaves =0  
            work_location=request.POST.get('work_location')


            # otherleaves=request.POST.get('otherleaves')

            if 'add_hr' in request.POST:
                
                employee_logins=Login(user_name=uname,password=pwd,user_type=1,f_name=f_name,l_name=l_name,
                                      dob=dob,mobile=phoneNo,email=mailid,address=Address,crt_date=datetime.now().date(),image='static/uploads/images.jpg',activation='Active',work_location=work_location)
                if len(Login.objects.filter(user_name=uname))>0:
                    pass
                else:
                    employee_logins.save()
                employee=Login.objects.filter(user_name=uname)
                emp_id=employee[0].id
                employement=''
                team=''
                taken=0
                remaining=int(sivckLeaves)+int(otherleaves)
                employee_detail=EmpDesk(login_id=emp_id,f_name=f_name,l_name=l_name,emp_type=1,
                                        employment=employement,gender=gender,email=mailid,doj=DOJ,dob=dob,
                                        mobile=phoneNo,mobile_alt=AltPhoneNo,address=Address,salary=salary,
                                        bank_name=bankName,account_number=acctNo,ifsc=ifsc_code,branch=branch,hr_id='',
                                        status=1,crt_date=datetime.now().date(),team_name=teamName,current_project=CurrProject,
                                        leave_taken=taken,leave_remaining=remaining,designations=designation,manager_id=manager,managers='',activation='Active')
                if len(EmpDesk.objects.filter(login_id=emp_id))>0:
                    pass 
                else:
                    employee_detail.save()
                name=request.session['name']
                DOJ = datetime.strptime(DOJ, "%Y-%m-%d")
                emp_name=f_name+l_name
                # add_to_project_team(request,manager_name,CurrProject,emp_name, emp_id,designation)
                
                reset_date=DOJ+timedelta(days=365)
                
                leave = LeaveDetails(emp_id=emp_id,remaining=otherleaves,taken=0,note='',name=f_name,sick_day=sivckLeaves,work_from_home=0,days_allowed=otherleaves,user_type=1,reset_date=reset_date,hr_id=emp_id)
                leave.save()
                employees=EmpDesk.objects.filter(emp_type='1',hr_id=emp_id)
            if 'add_mngr' in request.POST:
                manager_type=request.POST.get('manager_type')
                office_manager=request.POST.get('office_manager')
                employee_logins=Login(user_name=uname,password=pwd,user_type=manager_type,f_name=f_name,l_name=l_name,
                                      dob=dob,mobile=phoneNo,email=mailid,address=Address,crt_date=datetime.now().date(),image='static/uploads/images.jpg',activation='Active',work_location=work_location,office_manager=office_manager)
                if len(Login.objects.filter(user_name=uname))>0:
                    pass
                else:
                    employee_logins.save()
                employee=Login.objects.filter(user_name=uname)
                emp_id=employee[0].id
                employement=''
                team=''
                taken=0
                remaining=int(sivckLeaves)+int(otherleaves)
                employee_detail=EmpDesk(login_id=emp_id,f_name=f_name,l_name=l_name,emp_type=manager_type,
                                        employment=employement,gender=gender,email=mailid,doj=DOJ,dob=dob,
                                        mobile=phoneNo,mobile_alt=AltPhoneNo,address=Address,salary=salary,
                                        bank_name=bankName,account_number=acctNo,ifsc=ifsc_code,branch=branch,hr_id=hr_id,
                                        status=1,crt_date=datetime.now().date(),team_name=teamName,current_project=CurrProject,
                                        leave_taken=taken,leave_remaining=remaining,designations=designation,manager_id=emp_id,
                                        managers='',activation='Active')
                if len(EmpDesk.objects.filter(login_id=emp_id))>0:
                    pass 
                else:
                    employee_detail.save()
                name=request.session['name']
                DOJ = datetime.strptime(DOJ, "%Y-%m-%d")
                emp_name=f_name+l_name
                # add_to_project_team(request,manager_name,CurrProject,emp_name, emp_id,designation)
                
                reset_date=DOJ+timedelta(days=365)
                
                leave = LeaveDetails(emp_id=emp_id,remaining=otherleaves,taken=0,note='',name=f_name,sick_day=sivckLeaves,work_from_home=0,days_allowed=otherleaves,user_type=1,reset_date=reset_date,hr_id=hr_id)
                leave.save()
                employees=EmpDesk.objects.filter(emp_type='1',hr_id=emp_id)
                manager=Manager(emp_id=emp_id, name= (f_name+ ' ' +l_name),  hr_id=hr_id)
                manager.save()
        if 'Admin_Edit_Hr' in request.POST:
            request.session['edit_emp']=request.POST.get('Admin_Edit_Hr')
            return redirect('../superadmin/Admin_Edit_Hr')
        if 'Admin_Edit_Manager' in request.POST:
            request.session['edit_emp']=request.POST.get('Admin_Edit_Manager')
            return redirect('../superadmin/Admin_Edit_Manager')

        hr=EmpDesk.objects.filter(emp_type='1')
        manager=EmpDesk.objects.filter(emp_type='2')
        office_manager=Login.objects.filter(user_type='5')
        return render(request, 'Admin_user.html',{'hr':hr ,'manager':manager,'office_manager':office_manager})

def admin_empDetails(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.method=='GET':
        current_date=datetime.now().date()
        month=current_date.month
        year=current_date.year
        day=current_date.day
        print(current_date,year)
        request.session['emp_detail_date']=str(current_date)
    empdetails=EmpDesk.objects.filter(login_id=request.session['emp_details']).first
    if 'prev' in request.POST:
        current_date=request.session['emp_detail_date']
        print(current_date)
        current_date=datetime.strptime(current_date, '%Y-%m-%d')
        year = current_date.year - (current_date.month == 1)
        month = current_date.month - 1 if current_date.month > 1 else 12
        day = current_date.day

        # Adjust for months with fewer days
        while True:
            try:
                current_date = datetime(year, month, day)
                break
            except ValueError:
                day -= 1
        print(year,month,current_date)
        current_date=current_date.strftime('%Y-%m-%d')
        request.session['emp_detail_date']=str(current_date)
    elif 'next' in request.POST:
        current_date=request.session['emp_detail_date']
        print(current_date)
        current_date=datetime.strptime(current_date, '%Y-%m-%d')
        year = current_date.year + (current_date.month == 12)
        month = current_date.month + 1 if current_date.month < 12 else 1
        day = current_date.day

        
        while True:
            print(year, month, day)
            try:
                current_date = datetime(year, month, day)
                break
            except ValueError:
                day -= 1
        print(year,month,current_date)
        current_date=current_date.strftime('%Y-%m-%d')
        request.session['emp_detail_date']=str(current_date)

    report_data=Empdata.objects.annotate(start_datetime=Cast('start', DateField()),end_datetime=Cast('end', DateField())).filter(Q(emp_id=request.session['emp_details'],start_datetime__month=month,start_datetime__year=year,statushr='1')|Q(emp_id=request.session['emp_details'],end_datetime__month=month,end_datetime__year=year,statushr='1'))
    week1=[]
    week2=[]
    week3=[]
    week4=[]
    week5=[]
    week6=[]
    for i in report_data:
        first_day_of_month = (i.start_datetime).replace(day=1)
        week_number_of_first_day = first_day_of_month.isocalendar()[1]
        current_week_within_month = i.start_datetime.isocalendar()[1] - week_number_of_first_day +1
        if current_week_within_month==1:
            week1.append(i)
            week1_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==2:
            week2.append(i)
            week2_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==3:
            week3.append(i)
            week3_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==4:
            week4.append(i)
            week4_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==5:
            week5.append(i)
            week5_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==6:
            week6.append(i)
            week6_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
    weekly_data=[]
    weekly_performance=[]
    weekly_tasks=[]
    if len(week1)>0:
        start=week1[0].start
        end=week1[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)


        weekly_tasks.append(task)
        weekly_data.append(week1)
        weekly_performance.append(week1_comment_performance)
    if len(week2)>0:
        start=week2[0].start
        end=week2[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week2)
        weekly_performance.append(week2_comment_performance)
    if len(week3)>0:
        start=week3[0].start
        end=week3[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)

        
        weekly_tasks.append(task)
        weekly_data.append(week3)
        weekly_performance.append(week3_comment_performance)
    if len(week4)>0:
        start=week4[0].start
        end=week4[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)

        
        weekly_tasks.append(task)
        weekly_data.append(week4)
        weekly_performance.append(week4_comment_performance)
    if len(week5)>0:
        start=week5[0].start
        end=week5[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)

        
        weekly_tasks.append(task)
        weekly_data.append(week5)
        weekly_performance.append(week5_comment_performance)
    if len(week6)>0:
        start=week6[0].start
        end=week6[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)

        
        weekly_tasks.append(task)
        weekly_data.append(week6)
        weekly_performance.append(week6_comment_performance)    
    print(len(weekly_data),'weekly_data')
    weekly_data=zip(weekly_data,weekly_performance,weekly_tasks)
    return render(request, 'Admin_EmpDetails.html',{'month':month,'year':year,'empdetails':empdetails,'weekly_data':weekly_data})

def admin_timesheet(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    start_date=request.session['start_date']
    end_dt=request.session['end_date']
    if 'prev' in request.POST:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date=start_date-timedelta(days=7)
        end_dt = datetime.strptime(end_dt, '%Y-%m-%d')
        end_dt=end_dt-timedelta(days=7)
        request.session['start_date']= str(start_date.date())
        request.session['end_date']=str(end_dt.date())
        start_date=str(start_date.date())
        end_dt=str(end_dt.date())
    elif 'next' in request.POST:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date=start_date+timedelta(days=7)
        end_dt = datetime.strptime(end_dt, '%Y-%m-%d')
        end_dt=end_dt+timedelta(days=7)
        request.session['start_date']= str(start_date.date())
        request.session['end_date']=str(end_dt.date())
        start_date=str(start_date.date())
        end_dt=str(end_dt.date())
    print(start_date)
    with connection.cursor () as cursor:
        cursor.execute (fr"get_timesheet '{start_date}'")
        print(f"get_timesheet '{start_date}")
        data = dictfetchall (cursor)
    # Close the cursor object
        cursor.close ()

    
    return render(request, 'Admin_timesheet.html',{'data':data})

def Admin_notification(request):

    return render(request, 'Admin_notification.html')

def Admin_Edit_Hr(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="4":
        
        
        if request.method=='POST':
            f_name=request.POST.get('fname')
            l_name=request.POST.get('lname')
            mailid=request.POST.get('mailId')
            dob=request.POST.get('DOB')
            print(dob,'*********************************')
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d')
                dob = dob.strftime('%Y-%m-%d')  
            except:
                # dob = datetime.strptime(dob, '%y-%m-%d')
                dob = dob
            

            designation=request.POST.get('designation')
            gender=request.POST.get('gender')
            phoneNo=request.POST.get('phoneNo')
            AltPhoneNo=request.POST.get('AltPhoneNo')
            leave = request.POST.get('leave')
            sickleave = request.POST.get('sickleave')
                
            DOJ=request.POST.get('DOJ')
            print(DOJ,'----------------------------')
            try:
                DOJ = datetime.strptime(DOJ, '%Y-%m-%d')
                DOJ = DOJ.strftime('%Y-%m-%d')  
            except:
                # dob = datetime.strptime(dob, '%y-%m-%d')
                DOJ = DOJ
            salary=request.POST.get('salary')
            bankName=request.POST.get('bankName')
            acctNo=request.POST.get('acctNo')
            ifsc_code=request.POST.get('ifsc_code')
            branch=request.POST.get('branch')
            
            
            teamName=request.POST.get('teamName')
            manager=request.POST.get('manager')
            HR=request.POST.get('HR')
            Address=request.POST.get('Address')
            if 'cancel_emp' in request.POST:
                return redirect('../../hr/HR_empList')
            if 'edit_emp' in request.POST:
                EmpDesk.objects.filter(login_id = request.session['edit_emp']).update(f_name=f_name,l_name=l_name,gender=gender,
                                                                                      designation=designation,
                                                                                      email=mailid, mobile=phoneNo,
                                                                                      mobile_alt=AltPhoneNo,address=Address,
                                                                                      salary=salary,bank_name=bankName,
                                                                                      account_number=acctNo,ifsc=ifsc_code,
                                                                                      branch=branch,doj=DOJ,dob=dob,
                                                                                      team_name=teamName,designations=designation,
                                                                                      )
                
                leaveDetails = LeaveDetails.objects.filter(emp_id = request.session['edit_emp']).update(name=f_name,sick_day = sickleave, days_allowed = leave)
                updates=Login.objects.filter(id=request.session['edit_emp']).update(f_name=f_name,l_name=l_name,dob=dob,mobile=phoneNo ,email=mailid ,address=Address)
                user=Login.objects.get(id=request.session['edit_emp']).user_name
                updates=Attendance.objects.filter(user=user).update(name=f_name)
                updates=Payroll.objects.filter(user_name=user).update(employee=(f_name + l_name))
                updates=Empdata.objects.filter(emp_id=request.session['edit_emp']).update(name=f_name )
                updates=EmpLeaves.objects.filter(emp_id=request.session['edit_emp']).update(emp_name=f_name )
                updates=Notifications.objects.filter(emp_id=request.session['edit_emp']).update(emp_name=f_name )
       
        name=request.session['name']
        data = EmpDesk.objects.annotate(doj_s=Cast('doj', output_field=CharField()),dob_s=Cast('dob', output_field=CharField())).filter(login_id = request.session['edit_emp'])
        data = data[0] 
        manager = Login.objects.filter(user_type='2')
        leaveDetails = LeaveDetails.objects.filter(emp_id = request.session['edit_emp'])
        leaveDetails=leaveDetails[0]
        # print(leaveDetails,leaveDetails.sick_day)
        managers=Manager.objects.all()
        HR = Login.objects.filter(user_type='1')
        designation = DesignationMaster.objects.all()     
        print(HR[0].id,type(HR[0].id),data.hr_id,(type(data.hr_id)))   
        return render(request,'Admin_edit_HR.html',{'name':name,'leaveDetails':leaveDetails, 'employee':data,'managers':managers,'manager':manager, 'hr':HR, 'designation':designation})

def Admin_Edit_Manager(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response

    if request.session['user']=="4":
        
        if request.method=='POST':
            f_name=request.POST.get('fname')
            l_name=request.POST.get('lname')
            mailid=request.POST.get('mailId')
            dob=request.POST.get('DOB')
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d')
                dob = dob.strftime('%Y-%m-%d')  
            except:
                # dob = datetime.strptime(dob, '%y-%m-%d')
                dob = dob
            

            designation=request.POST.get('designation')
            gender=request.POST.get('gender')
            phoneNo=request.POST.get('phoneNo')
            AltPhoneNo=request.POST.get('AltPhoneNo')
            leave = request.POST.get('leave')
            sickleave = request.POST.get('sickleave')
                
            DOJ=request.POST.get('DOJ')
            try:
                DOJ = datetime.strptime(DOJ, '%Y-%m-%d')
                DOJ = DOJ.strftime('%Y-%m-%d')  
            except:
                # dob = datetime.strptime(dob, '%y-%m-%d')
                DOJ = DOJ
            salary=request.POST.get('salary')
            bankName=request.POST.get('bankName')
            acctNo=request.POST.get('acctNo')
            ifsc_code=request.POST.get('ifsc_code')
            branch=request.POST.get('branch')
            
            teamName=request.POST.get('teamName')
            
            HR=request.POST.get('HR')
            Address=request.POST.get('Address')
            if 'cancel_emp' in request.POST:
                return redirect('../../hr/HR_empList')
            if 'edit_emp' in request.POST:
                EmpDesk.objects.filter(login_id = request.session['edit_emp']).update(f_name=f_name,l_name=l_name,gender=gender,
                                                                                      designation=designation,
                                                                                      email=mailid, mobile=phoneNo,
                                                                                      mobile_alt=AltPhoneNo,address=Address,
                                                                                      salary=salary,bank_name=bankName,
                                                                                      account_number=acctNo,ifsc=ifsc_code,
                                                                                      branch=branch,doj=DOJ,dob=dob,
                                                                                      team_name=teamName,designations=designation,
                                                                                      hr_id=HR)
                
                leaveDetails = LeaveDetails.objects.filter(emp_id = request.session['edit_emp']).update(name=f_name,sick_day = sickleave, days_allowed = leave)
                updates=Login.objects.filter(id=request.session['edit_emp']).update(f_name=f_name,l_name=l_name,dob=dob,mobile=phoneNo ,email=mailid ,address=Address)
                user=Login.objects.get(id=request.session['edit_emp']).user_name
                updates=Attendance.objects.filter(user=user).update(name=f_name)
                updates=Payroll.objects.filter(user_name=user).update(employee=(f_name + l_name))
                updates=Empdata.objects.filter(emp_id=request.session['edit_emp']).update(name=f_name )
                updates=EmpLeaves.objects.filter(emp_id=request.session['edit_emp']).update(emp_name=f_name )
                updates=Notifications.objects.filter(emp_id=request.session['edit_emp']).update(emp_name=f_name )
       
        name=request.session['name']
        data = EmpDesk.objects.annotate(doj_s=Cast('doj', output_field=CharField()),dob_s=Cast('dob', output_field=CharField())).filter(login_id = request.session['edit_emp'])
        data = data[0] 
        manager = Login.objects.filter(user_type='2')
        leaveDetails = LeaveDetails.objects.filter(emp_id = request.session['edit_emp'])
        leaveDetails=leaveDetails[0]
        # print(leaveDetails,leaveDetails.sick_day)
        managers=Manager.objects.all()
        HR = Login.objects.filter(user_type='1')
        designation = DesignationMaster.objects.all()     
        print(HR[0].id,type(HR[0].id),data.hr_id,(type(data.hr_id)))   
        return render(request,'Admin_edit_Manager.html',{'name':name,'leaveDetails':leaveDetails, 'employee':data,'managers':managers,'manager':manager, 'hr':HR, 'designation':designation})

def Admin_Project_task(request):
    try:
        if request.session['user']=="4":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="4":
        pass
    else:
        response=HttpResponseRedirect('../../')
        return response
    task_id=request.session['project_name']
    if 'add_Task' in request.POST:

        project_name=request.session['project_name']
        project_id=project_name
        print(project_name)
        try:
            team_id=Project_team.objects.filter(project=project_name).first().team
        except:
            team_id=''
        task_heading=request.POST.get('task_heading')
        description=request.POST.get('task')

        description = description.split('\n')

        # Add <br> at the end of each line
        description = [line + '<br>' for line in description]

        # Join the lines back together with <br>
        description = ''.join(description)

        assigning_date=date.today()
        target_date=request.POST.get('date')
        task_crew=request.POST.getlist('task_crew')
        task_type=request.POST.get('type')
        priority=request.POST.get('priority')
        print(task_type,task_crew)
        complete_date=''
        manager_id=request.session['id']
        hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
        status='Task List'
        crt_date=datetime.now()
        projec_task_id=Tasks.objects.filter(project_id=project_id)
        projec_task_id=len(projec_task_id)
        projec_task_id=projec_task_id+1

        phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project_name)
        phase=[x.phase_float for x in phase_value]
        phase=max(phase)
        phase=int(phase)
        version=[x.version_float for x in phase_value]
        version=max(version)
    
        Tasks.objects.create(project_id=project_id,team_id=team_id,description=description,assigning_date=assigning_date,
            target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date,
            ui=' '  ,database=' ' ,backend=' ',projec_task_id=projec_task_id,phase=phase,project_version=version,task_heading=task_heading,
            task_type=task_type, priority=priority)

        task_id=Tasks.objects.filter(project_id=project_id,description=description,assigning_date=assigning_date,
            target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date).first()
        task_id=task_id.id
        
        for employee in task_crew:
            obj=TaskCrew.objects.filter(task_id=task_id,employee_name=employee)
            if len(obj)>0:
                pass
            else:
                TaskCrew.objects.create(task_id=task_id,employee_name=employee,create_date=datetime.now(),status='Task List')
        if True:
            print(request.FILES)
            uploaded_files = request.FILES.getlist('attachments')
            image_name=[]
            print(uploaded_files)
            for uploaded_file in uploaded_files:
                if uploaded_file is not None:
                    id_gen=str(task_id)
                    image=id_gen+uploaded_file.name
                    image=image.replace(' ','')
                    file_path = fr'static/uploads/task_files/{image}'
                    with open(file_path, 'wb') as file:
                        for chunk in uploaded_file.chunks():
                            file.write(chunk)
                    TaskFiles.objects.create(task_id=task_id,file_name=image,create_date=datetime.now())
        else:
            pass
        
        TasksLogs.objects.create(project_id=project_id, task_id=task_id, from_status='Task List', to_status='Task List', 
            assigning_date=assigning_date, target_date=target_date, complte_date=complete_date, manager_id=manager_id, user_id=request.session['id'], crt_date=crt_date,)
    
    task_ids=Tasks.objects.filter(project_id=request.session['project_name'])
    task_ids=[x.id for x in task_ids] 
    project_team=Project_team.objects.filter(project=request.session['project_name']) 
    chats=TasksChats.objects.filter(task_id__in=task_ids).annotate(tasks_id=Cast('task_id', output_field=IntegerField())).exclude(description=None).order_by('id')
    last_id=[x.id for x in chats]
    try:
        last_id=last_id[-1]
    except:
        last_id=0
    request.session['last_id']=last_id

    tasks_list=Tasks.objects.filter(status='Task List',project_id=request.session['project_name'])
    development=Tasks.objects.filter(status='Development',project_id=request.session['project_name'])
    completed=Tasks.objects.filter(status='Completed',project_id=request.session['project_name'])
    # print(chats)

    
    employees=EmpDesk.objects.filter(activation='Active')
    
    tasks_list=Tasks.objects.filter(status='Task List',project_id=request.session['project_name']).order_by('-id')
    task_list=[]
    task_list_logs=[]
    logs=[]
    task_chat=[]
    task_crew=[]

    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]
    all_crew=[]
    for i in tasks_list:
        all_crews=[]
        tasks_list_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        tasks_list_log=len(tasks_list_logs)
        task_list.append(i)
        task_list_logs.append(tasks_list_log+1)
        chat=TasksChats.objects.filter(task_id=i.id)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        for cr in crews:
            if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)

    tasks_list=zip(task_list,task_list_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments, all_crew)        

    developments=Tasks.objects.filter(status='Development',project_id=request.session['project_name']).order_by('-id')
    development=[]
    developments_logs=[]
    logs=[]
    task_chat=[]

    task_crew=[]

    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]
    all_crew=[]
    for i in developments:
        all_crews=[]
        development_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        development_log=len(development_logs)
        development.append(i)
        developments_logs.append(development_log+1)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        for cr in crews:
            if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)
    development=zip(development,developments_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments,all_crew)  
    
    completeds=Tasks.objects.filter(status='Completed',project_id=request.session['project_name']).order_by('-id')
    completed=[]
    completedt_logs=[]
    logs=[]
    task_chat=[]
    
    task_crew=[]

    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]
    all_crew=[]
    for i in completeds:
        all_crews=[]
        completed_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed').order_by('id')
        completed_log=len(completed_logs)
        completed.append(i)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))   
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))    
        completedt_logs.append(completed_log+1)
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        for cr in crews:
            all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)
    completed=zip(completed,completedt_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments,all_crew)
    
    project_team_task=[x.employee_name for x in project_team]

    return render(request, "admin_Project_task.html" ,{'project_team_task':project_team_task,'employees':employees,'project_team':project_team, 'tasks_list':tasks_list, 'development':development, 'completed':completed,'chats':chats})

def manage_attendance(request,i):
        all_dates = get_dates(i.from_dt, i.to_dt)
        print(all_dates,'all_dates------******************')
        user = Login.objects.get(id=i.emp_id).user_name
        try:
            user = Login.objects.get(id=i.emp_id).user_name
        except:
            user=''
        pl=i.paid_leaves
        try:
            pl=float(pl)
        except:
            pl=0
        leave_flag=0
        for j in  all_dates:
            day=j.day
            leave_month=j.month
            leave_year=j.year
            day='day'+str(day)
            print(user,'ddddddddddddddddddddddddddd')
            att=Attendance.objects.filter(user=user,month=leave_month,year=leave_year,).values().first()
            print(att,'att')
            if att[day]  == 'PL' or att[day]  == 'UL'  or att[day]  == 'SL':
                Attendance.objects.filter(user=user,month=leave_month,year=leave_year).update(**{day: ''})
           
            
       

        return 0

def get_dates(start_date, end_date):
    dates = []
    try:
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
    except:
        pass
    try:
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
    except:
        pass

    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

def weekdates():
    start_date=datetime.now().date()
    end_date=datetime.now().date()
    for i in range(8):
        if start_date.weekday()==0:
            starts=start_date
        else:
            start_date=start_date- timedelta(days=1, hours=0)
        if end_date.weekday()==6:
            end_dts=end_date
        else:
                end_date=end_date + timedelta(days=1, hours=0)
    start_date=starts
    end_date=end_dts
    return(start_date,end_date)

def Admin_phase(request):
    message=''
    project=request.session['project_name']
    projectdetails=ProjectDetails.objects.filter(project_name=project)
    phaseversion=PhaseVersion.objects.filter(project=project)
    if len(phaseversion)==0:
        PhaseVersion.objects.create(project=project, phase='1', version='1.0', start_date=datetime.now(), create_date=datetime.now(),time_period='2')
        # Versions.objects.create(project=project,version='1.0',create_date=datetime.now()) 
    version=Versions.objects.filter(project=project)
    if len(version)==0:
        Versions.objects.create(project=project,version='1.0',create_date=datetime.now()) 
    if request.method=='POST':
        if 'phase' in request.POST:
            time_period=request.POST.get('time_period')
            start_period=datetime.now()
            end_period=(start_period+timedelta(days=int(time_period)*7)).date()
            
            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                version_value=Versions.objects.annotate(version_float=Cast('version', output_field=FloatField())).filter(project=project)
                version=[x.version_float for x in version_value]
                version=max(version)
            except:
                phase=0
                version=1.0

            try:
                phase_data=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project,version_float=version,phase_float=phase).order_by('-phase_float').first()
                end_date=phase_data.start_date
                end_date=datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S.%f')
                end_date=(end_date+timedelta(days=int(phase_data.time_period)*7)).date()
                
                end_date=(end_date-datetime.now().date()).days
                
            except:
                end_date=0

            # phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project,version_float=version)
            # phase=[x.phase_float for x in phase_value]
            # phase=max(phase)
            new_phase=phase+1
            new_phase=int(new_phase)
            
            if end_date<3:
                message=''
                PhaseVersion.objects.create(project=project,version=version,phase=new_phase,start_date=datetime.now()  ,create_date=datetime.now(),time_period=time_period,end_date=end_period)  
            else:
                message='You can not create a new phase until two days before the end date of the current phase.'

        elif 'add_Task' in request.POST:

            project_name=request.session['project_name']
            project_id=project_name
            print(project_name)
            try:
                team_id=Project_team.objects.filter(project=project_name).first().team
            except:
                team_id=''
            task_heading=request.POST.get('task_heading')
            description=request.POST.get('task')

            description = description.split('\n')

        
            description = [line + '<br>' for line in description]

            # Join the lines back together with <br>
            description = ''.join(description)

            assigning_date=date.today()
            target_date=request.POST.get('date')
            task_crew=request.POST.getlist('task_crew')
            task_type=request.POST.get('type')
            priority=request.POST.get('priority')
            print(task_type,task_crew)
            complete_date=''
            manager_id=request.session['id']
            assignee=str(Login.objects.get(id=request.session['id']).f_name)+str(Login.objects.get(id=request.session['id']).l_name)
            hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
            status='Task List'
            crt_date=datetime.now()
            projec_task_id=Tasks.objects.filter(project_id=project_id)
            projec_task_id=len(projec_task_id)
            projec_task_id=projec_task_id+1

            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project_name)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                phase=int(phase)
                version=[x.version_float for x in phase_value]
                version=max(version)
            except:
                phase=1
                version=1.0

            Tasks.objects.create(project_id=project_id,team_id=team_id,description=description,assigning_date=assigning_date,
                target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date,
                ui=' '  ,database=' ' ,backend=' ',projec_task_id=projec_task_id,phase=phase,project_version=version,task_heading=task_heading,
                task_type=task_type, priority=priority,assignee=assignee)

            task_id=Tasks.objects.filter(project_id=project_id,description=description,assigning_date=assigning_date,
                target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date).first()
            task_id=task_id.id
            
            for employee in task_crew:
                obj=TaskCrew.objects.filter(task_id=task_id,employee_name=employee)
                if len(obj)>0:
                    pass
                else:
                    TaskCrew.objects.create(task_id=task_id,employee_name=employee,create_date=datetime.now(),status='Task List')
            if True:
                print(request.FILES)
                uploaded_files = request.FILES.getlist('attachments')
                image_name=[]
                print(uploaded_files)
                for uploaded_file in uploaded_files:
                    if uploaded_file is not None:
                        id_gen=str(task_id)
                        image=id_gen+uploaded_file.name
                        image=image.replace(' ','')
                        file_path = fr'static/uploads/task_files/{image}'
                        with open(file_path, 'wb') as file:
                            for chunk in uploaded_file.chunks():
                                file.write(chunk)
                        TaskFiles.objects.create(task_id=task_id,file_name=image,create_date=datetime.now())
            else:
                pass
            
            TasksLogs.objects.create(project_id=project_id, task_id=task_id, from_status='Task List', to_status='Task List', 
                assigning_date=assigning_date, target_date=target_date, complte_date=complete_date, manager_id=manager_id, user_id=request.session['id'], crt_date=crt_date,)
            

        elif 'version' in request.POST:
            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                version=[x.version_float for x in phase_value]
                version=max(version)
                version=version+0.1
                version = round(version, 1)
                # phase=1.0
                Versions.objects.create(project=project,version=version,create_date=datetime.now())  
            except:
                pass  


            # phaseversion=PhaseVersion.objects.filter(project=project)
    phases=[]
    tasks=[]
    team=[]
    versions  = PhaseVersion.objects.filter(project=project)
    versions=[x.version for x in versions]
    versions = [float(version) for version in versions]
    versions = sorted(set(versions))
    # print(versions,'-----------------')
    versions = [str(version) for version in versions]
    versions.reverse()
    version=[]
    employees=EmpDesk.objects.filter(activation='Active')
    for h in versions:
        phase= PhaseVersion.objects.filter(project=project,version=h).order_by('-id')
        phases=[]
        for i in  phase:
            start_period=str(i.start_date)
            print(start_period)
            try:
                start_period=datetime.strptime(start_period,'%Y-%m-%d')
            except:
                start_period=datetime.strptime(start_period,'%Y-%m-%d %H:%M:%S.%f')

            end_period=(start_period+timedelta(days=int(i.time_period)*7)).date()
            start_period=start_period.date()
            task=Tasks.objects.filter(project_id=project,phase=i.phase,project_version=h).order_by('-id')
            tasks=[]
            for j in task:
                crews=[]
                crew=TaskCrew.objects.filter(task_id=j.id)
                if len(crew)==0:
                    crew=Project_team.objects.filter(project=project)
                task_chat=TasksChats.objects.filter(task_id=j.id)
                task_logs=TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=j.id)
                attachments=TaskFiles.objects.filter(task_id=j.id)

                for cr in crew:
                    if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                        crews.append(cr.employee_name)
                for em in employees:
                    if em.email in crews:
                        pass
                    else:
                        crews.append(em.email)
                l=[j,crew,task_chat,task_logs,attachments,crews]
                tasks.append(l)
                l=team
            phases.append([i,tasks,end_period ,start_period])
        version.append(phases)
    
    project_team=Project_team.objects.filter(project=request.session['project_name']) 
    project_team_task=[x.employee_name for x in project_team]
    current_version_value=Versions.objects.annotate(version_float=Cast('version', output_field=FloatField())).filter(project=project)
    current_version=[x.version_float for x in current_version_value]
    current_version=max(current_version)
    current_phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
    current_phase=[x.phase_float for x in current_phase_value]
    current_phase=int(max(current_phase)+1)
    return render(request,"Admin_phase.html",{'current_phase':current_phase,'message':message,'version':version,'employees':employees,'project_team_task':project_team_task,'current_version':current_version})
 

def change_activation(request):
    data= request.GET.get('value')
    print(data,'value')
    emp_id= request.GET.get('emp_id')
    print(emp_id,'emp_id')
    Login.objects.filter(id=emp_id).update(activation=data)
    EmpDesk.objects.filter(login_id=emp_id).update(activation=data)
    return JsonResponse({'data': 'success'})
def reset_password(request):
    if request.method == 'POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        emp_id=request.session['reset_pwd']
        if password == confirm_password:
            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
            cipher_suite = Fernet(key)
            ciphered_text = cipher_suite.encrypt(bytes(password ,encoding='utf8')) 
            
            password=ciphered_text.decode()
            Login.objects.filter(id=emp_id).update(password=password)
    return render(request,'Admin_reset_password.html')










