from django.db import connection
from django.shortcuts import render,redirect
from django.http import HttpResponse
from mainlogin.models import Login
from HR.models import  Attendance,ProjectDetails,Manager,Project_team,EmpDesk,LeaveDetails,DesignationMaster,Payroll

from django.shortcuts import render
from Employee.models import Empdata,EmpLeaves
from ClientManager.models import Notifications,Ratings
from mainlogin.models import Login
import json
from datetime import datetime, timedelta, date
from django.db.models import F, Func, Value, DateField,CharField
from django.db.models.functions import Cast

import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponseRedirect
from cryptography.fernet import Fernet
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, Cast
from django.db.models import DateTimeField,FloatField,DateField
from django.db.models import Q
import smtplib
from email.message import EmailMessage
import ssl
# Create your views here.
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
# Create your views here.
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

def home(request):
    # try:
        if request.session['user']=="1":
        
            start_date,end_date=weekdates()
            request.session['start_date']=str(start_date)
            request.session['end_date']=str(end_date)        
            name=request.session['name']
            id=request.session['id']
            
            empl = EmpDesk.objects.filter(hr_id=request.session['id'],emp_type=3)
            
            notify = Notifications.objects.filter(hr='1',date=start_date,hr_id=request.session['id'])
            notify = len(notify)

            designations = EmpDesk.objects.filter(emp_type='3')
            dlist = {}
            label=[]
            data=[]
            for designation in designations:
                if designation.designations in label:
                    pass
                else:
                    label.append(designation.designations)
                    data.append(len(EmpDesk.objects.filter(designations=designation.designations, emp_type='3',hr_id=request.session['id'])))
                    

            pending = len(ProjectDetails.objects.filter(status='PENDING',hr_id=request.session['id']))
            completed = len(ProjectDetails.objects.filter(status='COMPLETE',hr_id=request.session['id']))
            # For Leave Expire
            leaves = EmpLeaves.objects.filter(status='Approved', hr_id=request.session['id']).order_by('-id')
            leaves_approved = [leave for leave in leaves if datetime.strptime(leave.from_dt, '%Y-%m-%d').date() > date.today()]
            images=[]
            for i in leaves_approved:
                try:
                    images.append(Login.objects.get(id=i.emp_id).image)
                except:
                    images.append(r'static/uploads/images.jpg')
            leaves_approved=zip(leaves_approved,images)
            
            leaves_denied=EmpLeaves.objects.filter(emp_id=id,status='Rejected',user_type='1')

            leaves_expired = []
            a_ = EmpLeaves.objects.all().values_list()
            for i in a_:
                print(i)
            projects=ProjectDetails.objects.filter(hr_id=request.session['id'])
            notifs = []
            noti = []
            notif = Notifications.objects.filter(hr='1',date=start_date,hr_id=request.session['id'])
            for i in notif:
                notifs.append(i)
                print(i,'-')
            try:
                noti.append(notifs[-1])
            except:
                pass
            try:
                noti.append(notifs[-2])
            except:
                pass
            try:
                noti.append(notifs[-3])
            except:
                pass
        
            emp_id = [i.emp_id for i in noti]
            images_data = Login.objects.filter(id__in=emp_id).values('image')
            image = [i['image'] for i in images_data]
            noti = zip(noti,image)

            days_allowed=[]
            for i in empl:
                try:
                    daysallowed=LeaveDetails.objects.get(emp_id=i.login_id).days_allowed
                    sick=LeaveDetails.objects.get(emp_id=i.login_id).sick_day
                    daysallowed=str(daysallowed)+' + '+str(sick)
                    days_allowed.append(daysallowed)
                except:
                    daysallowed=0
                    days_allowed.append(daysallowed)
            empl=zip(empl,days_allowed)
        
            dict={"pythn":90,"name":name,'noti':noti,'notify':notify, 'pending':pending,'complete':completed,'approved':leaves_approved,'denied':leaves_denied,'projects':projects,'employee':empl,'label':label,'data':data} 

            
            return render(request,'HR_dashboard.html',dict)
        else:
            response=HttpResponseRedirect('../../')
            return response  
    # except:  
    #     response=HttpResponseRedirect('../../')
    #     return response

def HR_approvedTimesheet(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        start_date=request.session['start_date']
        end_date=request.session['end_date']
        if request.method=="POST":
            
            if 'prev' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date.date()
                end_date=end_date.date()

                start_date=start_date- timedelta(days=7, hours=0)
                end_date=end_date- timedelta(days=7, hours=0)


                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)
        
            elif 'next' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date+ timedelta(days=7, hours=0)
                end_date=end_date+ timedelta(days=7, hours=0)
                start_date=start_date.date()
                end_date=end_date.date()
                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)

            elif 'approve' in request.POST:
                approved=request.POST.get('approve')
                approved=approved.split('|')
                print(approved)
                
                request.session['approved_emp_id'] = approved[0]
                request.session['start_dt'] = approved[1]
                request.session['end_dt'] = approved[2]
                print('hello vlog welcome to my guys')
                return redirect('../hr/HR_empTracker_Details')

        name=request.session['name']
        cursor = connection.cursor()
        print(f" hr_pending_timesheet '{start_date}','1','1','{request.session['id']}'")
        cursor.execute(f" hr_pending_timesheet_om_hr '{start_date}','1','1','{request.session['id']}'")    
        pending_timesheet = cursor.fetchall()   
        print(pending_timesheet)    
        data = Empdata.objects.all()
        name = request.session['name'] 
        pending=[]
        for i in pending_timesheet:
            designation=EmpDesk.objects.get(login_id=i[1]).designation
            pending.append({'name':i[13],'id':i[1],'designation':designation,'total':i[15]})
        start_date=str(start_date)
        end_date=str(end_date)
        return render(request,'HR_approvedTimesheet.html',{'name':name,'pending':pending, 'start_date': start_date, 'end_date': end_date})
    # else:
    #     response=HttpResponseRedirect('../../')
    #     return response


def HR_EditProfile(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        
        message1 = ''
        message = ''
        hrPro = EmpDesk.objects.filter(login_id=request.session['id'])
        hrPro = hrPro[0]
                
        if request.method == 'POST':
            if 'editProfile' in request.POST:

                data = EmpDesk.objects.filter(login_id=request.session['id'])
                data = data[0]
                data.email=request.POST.get('email')
                data.save(update_fields=['email'])
                data.mobile=request.POST.get('mobileNO')
                print(request.POST.get('mobileNo'))
                data.save(update_fields=['mobile'])
                data.address=request.POST.get('addr')
                data.save(update_fields=['address'])
                
                data = Login.objects.filter(id=request.session['id'])
                data = data[0]
                data.email=request.POST.get('email')
                data.save(update_fields=['email'])
                data.mobile=request.POST.get('mobileNo')
                data.save(update_fields=['mobile'])
                data.address=request.POST.get('addr')
                data.save(update_fields=['address'])
               
                if len(request.FILES) != 0:
                    data.image = request.FILES['profile_pic']
                    data.save(update_fields=['image'])
                    task=Login.objects.filter(id=request.session['id'])
                    request.session['profile_pic']=str(task[0].image)

            elif 'changePass' in request.POST:
                data = Login.objects.filter(id=request.session['id'])
                data = data[0]
                pwd=data.password
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
                        
                        data.password=ciphered_text.decode()
                        data.save(update_fields=['password'])
                elif pwd == request.POST.get('currPass'):
                    if request.POST.get('password') == request.POST.get('confirmPass'):
                        key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                        cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                        ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                        
                        data.password=ciphered_text
                        data.save(update_fields=['password']) 
                    else:
                        message1 = 'password and confirm password must be same.'

                else:
                    message = 'current password is incorrect'
        hrPro = EmpDesk.objects.filter(login_id=request.session['id'])
        hrPro = hrPro[0]
        name=request.session['name']
        return render(request,'HR_EditProfile.html',{'name':name,'hr':hrPro, 'message':message,'message1':message1})
    else:
        response=HttpResponseRedirect('../../')
        return response
def HR_notification(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        leave_details = EmpLeaves.objects.filter(from_dt=datetime.now().date(),status='Approved',hr_id=request.session['id'])
        for leaves in leave_details:
            obj=Notifications.objects.filter(message=f'{leaves.emp_name} is on leave today ({datetime.now().date()}) for {leaves.no_of_days} days',hr_id=request.session['id'])  
            if len(obj)>0:
                obj.delete()          
            notify = Notifications(emp_id=leaves.emp_id,message=f'{leaves.emp_name} is on leave today ({datetime.now().date()}) for {leaves.no_of_days} days',emp=0,hr=1,manager=0,date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
            notify.save()

        images=[]
        notiff = Notifications.objects.filter(hr='1',date=start_date,hr_id=request.session['id'])
        for i in notiff:
            image=Login.objects.filter(id=i.emp_id)
            image=image[0]
            images.append(image.image)
            
        notif = []
        notifs=[]
        
        for i in range(len(notiff)):
            notifs.append(notiff[i])
        for i in range(1,(len(notifs)+1)):
            notif.append(notifs[(-i)])
        images.reverse()
       
        notif=zip(notif,images)
        notify = []
        if request.method == 'POST':
            dts = request.POST.get('clearAll')
            notif=[]
            if 'clear' in request.POST:
                notify = Notifications.objects.filter(hr='1',date=start_date,hr_id=request.session['id'])
                for i in notify:
                    i.hr='2'
                    i.save(update_fields=['hr'])
                 
        
        name=request.session['name']
        return render(request,'HR_notification.html',{'name':name,'notif':notif,'notify':notify,'dts':start_date})
    else:
        response=HttpResponseRedirect('../../')
        return response
def HR_teamReport(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
    
        # for j in range(1,24):
        #     i= Login.objects.filter(id=j)
        #     obj=LeaveDetails.objects.filter(id=j)
        #     try:
        #         obj1=i[0]
        #     except:
        #         pass
        #     try:
        #         obj2=obj[0]
        #     except:
        #         pass
        #     try:
        #         obj2.user_type=obj1.user_type
        #     except:
        #         pass
        #     try:
        #         obj2.save(update_fields=['user_type'])
        #     except:
        #         pass

        managers=Manager.objects.filter(hr_id=request.session['id'])
        team_data=[] 
        projects=ProjectDetails.objects.filter(hr_id=request.session['id'])
        team=Project_team.objects.filter(hr_id=request.session['id']).order_by('id')
        team_data=Project_team.objects.filter(hr_id=request.session['id']).order_by('project')
        print(team_data)
        # for i in team:
        #     try:
        #         team_data.append({'team':i.team,'manager':i.manager,
        #                       'employee_name':str(EmpDesk.objects.get(login_id=i.employee_id).f_name)+" "+str(EmpDesk.objects.get(login_id=i.employee_id).l_name),
        #                       'employee_id':i.employee_id,'email':EmpDesk.objects.get(login_id=i.employee_id).email,'designation':i.designation,
        #                       'project':i.project,'crt_date':i.crt_date})
        #     except:
        #         pass
        
        name=request.session['name']
        employees=EmpDesk.objects.filter(emp_type='3',hr_id=request.session['id'])    
        leave=LeaveDetails.objects.filter(user_type=3,hr_id=request.session['id'])
        name=request.session['name']
        verifys=LeaveDetails.objects.filter(hr_id=request.session['id'])
        
        for verify in verifys:
            reset_date=verify.reset_date
            reset_date = datetime.strptime(reset_date, "%Y-%m-%d %H:%M:%S")
            today = datetime.now()
            print(today,'today',reset_date,'reset_date')
            print(str(today-reset_date).split(' ')[0])
            try:
                deltas=int(str(today-reset_date).split(' ')[0] )  
            except:
                deltas=0

           
            
            if deltas>0:
                verify.reset_date=reset_date+timedelta(days=365)
                verify.save(update_fields=['reset_date'])
                verify.days_allowed=10
                verify.save(update_fields=['days_allowed'])
                verify.sick_day=3
                verify.save(update_fields=['sick_day'])
                
                verify.taken=0
                verify.save(update_fields=['taken'])
                verify.remaining=13
                verify.save(update_fields=['remaining'])
        return render(request,'HR_teamReport.html',{'team_data':team_data,'name':name,'leave':leave,'manager':managers,'project':projects,'team':team,'employee':employees})
    else:
        response=HttpResponseRedirect('../../')
        return response

 
def HR_pendingTimesheet(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user'] == "1":
        start_date = request.session['start_date']
        end_date = request.session['end_date']
        obj = []
        totals = 0
        Name = ''
        names=''
        count = 0
        task = Empdata.objects.filter(start=start_date)
        for i in task:
            if i.name == Name:
                totals = totals+i.total
                continue
            else:
                
                obj.append(i)
                Name = i.name
                totals = i.total
        if request.method=="POST" and ('prev' in request.POST or 'next' in request.POST):
            
            if 'prev' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date.date()
                end_date=end_date.date()

                start_date=start_date- timedelta(days=7, hours=0)
                end_date=end_date- timedelta(days=7, hours=0)


                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)
        
            elif 'next' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date+ timedelta(days=7, hours=0)
                end_date=end_date+ timedelta(days=7, hours=0)
                start_date=start_date.date()
                end_date=end_date.date()
                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)
            obj = []
            totals = 0
            Name = []
            count = 0
            designations=[]
            t=[]
            task = Empdata.objects.filter(status=1,start=start_date)
            for i in task:
                print
                if i.emp_id in Name:
                    print(i.total)
                    totals = totals+i.total
                    continue
                else:
                    t.append(totals)
                    eid=i.emp_id
                    des=EmpDesk.objects.filter(login_id=eid)
                    designation=des[0].designations
                    designations.append(designation)               
                    obj.append(i)
                    Name.append(i.emp_id)
                    totals = i.total
                    print(i.total)
            t.append(totals)
            t=t[1:]
         
            obj = zip(obj,designations,t)


        elif request.method == "POST":
            
            e_id = 0
            if 'pending' in request.POST:
                print()

                emp_id=request.POST.get('pending')
                data=Empdata.objects.filter(emp_id=emp_id,start=start_date)

                if len(data)>0:
                    starts=data[0].start
                    emp_name=data[0].name
                    employee_id=data[0].emp_id
                    employee_start=data[0].start
                    employee_end=data[0].end
                    des=EmpDesk.objects.filter(login_id=emp_id)
                    designation=des[0].designations
                try:
                    img=Login.objects.get(id=emp_id).image
                except:
                    img=''
                
                try:
                    comments=Ratings.objects.get(emp_id=emp_id,startdate=start_date).employee_comment
                    tue_comm = Ratings.objects.get(emp_id=emp_id,startdate=start_date).emp_comm_tue
                    wed_comm = Ratings.objects.get(emp_id=emp_id,startdate=start_date).emp_comm_wed
                    thu_comm = Ratings.objects.get(emp_id=emp_id,startdate=start_date).emp_comm_thu
                    fri_comm = Ratings.objects.get(emp_id=emp_id,startdate=start_date).emp_comm_fri
                    sat_comm = Ratings.objects.get(emp_id=emp_id,startdate=start_date).emp_comm_sat
                    print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'try')
                except:
                    comments = ''
                    tue_comm = ''
                    wed_comm = ''
                    thu_comm = ''
                    fri_comm = ''
                    sat_comm = ''
                    print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'try')
                name = request.session['name']
                return render(request, 'HR_empTracker.html',{'comments':comments,'name': name,'img':img, 'data':data,'tue_comm':tue_comm,'wed_comm':wed_comm,'thu_comm':thu_comm,'fri_comm':fri_comm,'sat_comm':sat_comm,'date':starts,'emp_id':emp_id,'designation':designation,'count': count, 'start_date': str(start_date), 'end_date': str(end_date),'emp_name': emp_name,"employee_id":employee_id, 'employee_start':employee_start,'employee_end':employee_end })

            elif 'denied' in request.POST:
                
                
                emp_id=request.POST.get('denied')
                data=Empdata.objects.filter(emp_id=emp_id,status=1,start=start_date)
                starts=start_date
                if len(data)>0:
                    starts=data[0].start
                    emp_name=data[0].name
                    employee_id=data[0].emp_id
                    employee_start=data[0].start
                    employee_end=data[0].end
                emp_id = request.session['id']   
                name = request.session['name']
                

            

            elif 'Approve' in request.POST:
                emp_id=request.POST.get('empid')
                

                e_date= request.POST.get('Approve')
                print(emp_id,e_date)
                t = Empdata.objects.filter(status=4,emp_id=emp_id,start=e_date)
                j=t[0]
                for i in t:
                                    
                    i.statushr = 1
                    
                    
                    i.save(update_fields=['statushr'])
                    
                    task = Empdata.objects.all()
                name_of_emp=Login.objects.get(id=emp_id).f_name
                email=Login.objects.filter(id=emp_id)
                email=[x.email for x in email]
                
                manager_id=EmpDesk.objects.get(login_id=emp_id).manager_id
                manager_mail=Login.objects.get(id=manager_id).email
                email.append(manager_mail)
                sender = 'ats.ariespro@gmail.com'
                receivers = email

                receivers = email
                password = 'ahbfhcshjujvkgge'
                Subject= 'Timesheet Approved'

                message = f"""
                Hi {name_of_emp},   

                Your Timesheet for period {start_date} to {end_date}  is Approved by HR. 

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
                # server['cc']=manager_mail #'neelam.vohra@ariespro.com'
                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass    
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your Timesheet for Week ( {j.start} - {j.end} is Approved by the HR Today ({datetime.now().date()}) ',emp_name=j.name,date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
                    
            elif 'Deny' in request.POST:
                
                emp_id=request.POST.get('empid')
                e_id = request.POST.get('Deny')
                print(emp_id,e_id)
                t = Empdata.objects.filter(emp_id=emp_id,start=start_date)
                j=t[0]
                for i in t:
                    if i.statushr=='2':
                        i.delete()
                        notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your Timesheet for Week ( {j.start} - {j.end} is Discarded by the HR Today ({datetime.now().date()}) ',emp_name=j.name,date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                        notify.save()
                    else:
                        names=i.name
                        i.statushr = '2'
                        i.save(update_fields=['statushr'])
                        i.status = '2'
                        i.save(update_fields=['status'])
                    data = Empdata.objects.all()
                name_of_emp=Login.objects.get(id=emp_id).f_name
                email=Login.objects.filter(id=emp_id)
                email=[x.email for x in email]
                manager_id=EmpDesk.objects.get(login_id=emp_id).manager_id
                manager_mail=Login.objects.get(id=manager_id).email
                email.append(manager_mail)
                sender = 'ats.ariespro@gmail.com'
                receivers = email
                password = 'ahbfhcshjujvkgge'
                Subject= 'Timesheet Rejected'

                message = f"""
                Hi {name_of_emp},   

                Your Timesheet for period {start_date} to {end_date}  is Rejected by HR. 

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
                # server['cc']=manager_mail #'neelam.vohra@ariespro.com'
                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass 
                
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your Timesheet for Week ( {j.start} - {j.end} is rejected by the HR Today ({datetime.now().date()}) ',emp_name=j.name,date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
        totals = 0
        count = 0
        cursor = connection.cursor()
        print(f" hr_pending_timesheet '{start_date}','4','0','{request.session['id']}'")
        cursor.execute(f" hr_pending_timesheet '{start_date}','4','0','{request.session['id']}'")    
        pending_timesheet = cursor.fetchall()   
        print(pending_timesheet)    
        data = Empdata.objects.all()
        name = request.session['name'] 
        pending = []
        
        for i in pending_timesheet:
            designation=EmpDesk.objects.get(login_id=i[1]).designation
            pending.append({'name':i[13],'id':i[1],'designation':designation,'total':i[15]})
        return render(request, 'HR_pendingTimesheet.html', {'pending':pending,"data": data, "name": name, 'names':names, 'count': count, 'start_date': start_date, 'end_date': end_date})
    # else:
    #     response=HttpResponseRedirect('../../')
    #     return response

def HR_empList(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response

    if request.session['user']=="1":
        
        manager = Login.objects.filter(user_type='2')
        office_manager=Login.objects.filter(user_type='5')
        managers=manager[0].user_name
        HR = Login.objects.filter(user_type='1',work_location=Login.objects.get(id=request.session['id']).work_location)
        designation = DesignationMaster.objects.all()
        print('-----------method')
        print('-----------method',request.method)
        if request.method=="POST":
            print('hello----')
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
                print('1111111111111111111111111111111111111111')

                # otherleaves=request.POST.get('otherleaves')
            if 'add_emp' in request.POST:
                print('---------entered the ------------------a')
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
                office_manager=request.POST.get('office_manager')
                hr_id=request.session['id']
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
                
                # otherleaves=request.POST.get('otherleaves')
                work_location=request.POST.get('work_location')
                employee_logins=Login(user_name=uname,password=pwd,user_type=3,f_name=f_name,l_name=l_name,
                                      dob=dob,mobile=phoneNo,email=mailid,address=Address,crt_date=datetime.now().date(),
                                      image='static/uploads/images.jpg',activation='Active',work_location=work_location,office_manager=office_manager)
                if len(Login.objects.filter(user_name=uname))>0:
                    pass
                else:
                    employee_logins.save()
                employee=Login.objects.filter(user_name=uname)
                emp_id=employee[0].id
                employement=''
                team=''
                taken=0
                remaining=''
                employee_detail=EmpDesk(login_id=emp_id,f_name=f_name,l_name=l_name,emp_type=3,
                                        employment=employement,gender=gender,email=mailid,doj=DOJ,dob=dob,
                                        mobile=phoneNo,mobile_alt=AltPhoneNo,address=Address,salary=salary,
                                        bank_name=bankName,account_number=acctNo,ifsc=ifsc_code,branch=branch,hr_id=hr_id,
                                        status=1,crt_date=datetime.now().date(),team_name=teamName,current_project=CurrProject,
                                        leave_taken=taken,leave_remaining=remaining,designations=designation,manager_id=manager,managers=manager_name,activation='Active')
                if len(EmpDesk.objects.filter(login_id=emp_id))>0:
                    pass 
                else:
                    employee_detail.save()
                name=request.session['name']
                DOJ = datetime.strptime(DOJ, "%Y-%m-%d")
                emp_name=f_name+l_name
                add_to_project_team(request,manager_name,CurrProject,emp_name, emp_id,designation)
                
                reset_date=DOJ+timedelta(days=365)
                
                leave = LeaveDetails(emp_id=emp_id,remaining=otherleaves,taken=0,note='',name=f_name,sick_day=sivckLeaves,work_from_home=0,days_allowed=otherleaves,user_type=3,reset_date=reset_date,hr_id=request.session['id'])
                leave.save()
                employees=EmpDesk.objects.filter(emp_type='3',hr_id=request.session['id'])
                return render(request,'HR_empList.html',{'name':name,'employees':employees,'message':'New employee added !!!','managers':managers,'manager':manager, 'hr':HR, 'designation':designation})
                # return render(request,'HR_empList1.html',{'name':name,'employees':employees,'message':'New employee added !!!','managers':managers,'manager':manager, 'hr':HR, 'designation':designation})
            
            if 'add_hr' in request.POST:
                print('2222222222222222222222222222222222222222')
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
                print('333333333333333333333')
                work_location=Login.objects.get(id=request.session['id']).work_location
                manager_type=request.POST.get('manager_type')
                office_manager=request.POST.get('office_manager')
                client=request.POST.get('client_name')
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
                manager=Manager(emp_id=emp_id, name= (f_name+ ' ' +l_name),  hr_id=hr_id,client=client,office_manager=office_manager)
                manager.save()
            if 'Admin_Edit_Hr' in request.POST:
                request.session['edit_emp']=request.POST.get('Admin_Edit_Hr')
                return redirect('../hr/HR_Edit_Hr')
            if 'Admin_Edit_Manager' in request.POST:
                request.session['edit_emp']=request.POST.get('Admin_Edit_Manager')
                return redirect('../hr/HR_Edit_Manager')
            elif 'edit_emp' in request.POST:
                request.session['edit_emp'] = request.POST.get('edit_emp')
                return redirect('../../hr/HR_editEmp')
            elif 'activation' in request.POST:
                emp_id=request.POST.get('activation')
                stats=Login.objects.get(id=emp_id).activation
                if stats=='Active':
                    Login.objects.filter(id=emp_id).update(activation='Deactive')
                    EmpDesk.objects.filter(login_id=emp_id).update(activation='Deactive')
                else:
                    print('buttotn deactive')
                    EmpDesk.objects.filter(login_id=emp_id).update(activation='Active')
                    Login.objects.filter(id=emp_id).update(activation='Active')
                # stats=EmpDesk.objects.get(login_id=emp_id).activation
               
                
                pass
        
        empl=Login.objects.filter(work_location=Login.objects.get(id=request.session['id']).work_location)
        empl=[x.id for x in empl]
        employees=EmpDesk.objects.filter(hr_id=request.session['id'],emp_type='3').exclude(emp_type='1')
        name=request.session['name']
        hr_list=EmpDesk.objects.filter(emp_type='1')
        manager_list=EmpDesk.objects.filter(emp_type='2',login_id__in=empl)
        
        office_manager=Login.objects.filter(user_type='5')
        return render(request,'HR_empList.html',{'hr_list':hr_list ,'manager_list':manager_list ,'office_manager':office_manager,'name':name,'managers':managers,'employees':employees,'manager':manager, 'hr':HR, 'designation':designation})
        # return render(request,'HR_empList1.html',{'hr_list':hr_list ,'manager_list':manager_list ,'office_manager':office_manager,'name':name,'managers':managers,'employees':employees,'manager':manager, 'hr':HR, 'designation':designation})
    else:
        response=HttpResponseRedirect('../../')
        print(response)
        return response

def HR_leave(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        remaining_leaves=LeaveDetails.objects.filter(emp_id=request.session['id'])
        try:
            remaining_leaves=remaining_leaves[0]
        except:
            pass
        flag=0
        if request.method=='POST':
            
            if 'apply' in request.POST:

                leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
                
                empid=request.session['id']
             
                empname=request.session['name']
          
                leavetype=request.POST.get('type')
               
                fromdt=request.POST.get('from')
               
                todt=request.POST.get('to')
              
                daytype=request.POST.get('day')
               
                noofdays=request.POST.get('noofdays')
              
                reason=request.POST.get('reason')
              
                taken=leave_details[0].taken
              
                remaining=leave_details[0].remaining
              
                # leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
                # empid=request.session['id']
                # empname=request.session['name']
                # leavetype=request.POST.get('type')
                # fromdt=request.POST.get('from')
                # todt=request.POST.get('to')
                # daytype=request.POST.get('day')
                # noofdays=request.POST.get('noofdays')
                # reason=request.POST.get('reason')
                # taken=leave_details[0].taken
                # remaining=leave_details[0].remaining
                
               
               
                leave_details = EmpLeaves(emp_id=empid,emp_name=empname,leave_type=leavetype,from_dt=fromdt,to_dt=todt,day_type=daytype,no_of_days=noofdays,leave_taken=taken,remaining_leaves=remaining,reason=reason,status='Applied',date_applied=datetime.now().date(),user_type=1,valid_leaves=0)
                leave_details.save()
            
                notify = Notifications(emp_id=request.session['id'],message=f'{request.session["name"]} has applied for leave', date=start_date,current_date=datetime.now().date(), emp=0,hr=0,manager=1,hr_id=request.session['id']) 
                notify.save()
                sender = 'ats.ariespro@gmail.com'
                # receivers = "karan.rana@ariespro.com"
                receivers = "neelam.vohra@ariespro.com"
                password = 'ahbfhcshjujvkgge'
                Subject= 'Leave Application'
                message = f"""
                Hi Ma'am,
                - Leave Type: {leavetype}
                - Number of Days: {noofdays}
                - Date From: {fromdt}
                - Date To: {todt}
                - Note: {reason}.
                                    
                Thank you,
                {empname}
                        """
                server=EmailMessage()
                server['From']='Ariespro'
                server['To']=receivers
                server['Subject']=Subject
                server.set_content(message)
                context=ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    smtp.login(sender,password)
                    smtp.sendmail(sender,receivers,server.as_string())
                    
            flag=0
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
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass
            elif 'reject' in request.POST:
                emp_id=int(request.POST.get('reject'))
                print(emp_id)
                
                emp=EmpLeaves.objects.filter(id=emp_id)
                
                i=emp[0]
                if i.status=='Approved':
                    noofday=float(emp[0].no_of_days)
                    leave_start=emp[0].from_dt
                    leave_end=emp[0].to_dt
                    leave_start= datetime.strptime(leave_start, '%Y-%m-%d')
                    leave_end= datetime.strptime(leave_end, '%Y-%m-%d')
                    leave_holiday=get_holiday_in_leaves(leave_start,leave_end)
                    noofday=noofday-leave_holiday

                    if i.leave_type=='Sick Leave':
                        try:
                            paid_leave_revert=float(i.paid_leaves)
                        except:
                            paid_leave_revert=0
                        paid_leave_revert=paid_leave_revert-leave_holiday
                        leave_taken=float(EmpDesk.objects.get(login_id=i.emp_id).leave_taken)
                        leave_taken=leave_taken-paid_leave_revert
                        
                        if leave_taken<0:
                            leave_taken=0
                        leave_remaining=float(EmpDesk.objects.get(login_id=i.emp_id).leave_remaining)
                        leave_remaining=leave_remaining+paid_leave_revert
                        EmpDesk.objects.filter(login_id=i.emp_id).update(leave_taken=leave_taken,leave_remaining=leave_remaining)
                        try:
                            remaining=float(LeaveDetails.objects.get(emp_id=i.emp_id).remaining)
                        except:
                            remaining=0
                        remaining=remaining+paid_leave_revert
                        try:
                            sick_day=float(LeaveDetails.objects.get(emp_id=i.emp_id).sick_day)
                        except:
                            sick_day=0
                        sick_day=sick_day+paid_leave_revert
                        try:
                            taken=float(LeaveDetails.objects.get(emp_id=i.emp_id).taken)
                        except:
                            taken=0
                        taken=taken-paid_leave_revert
                        if taken<0:
                            taken=0
                        print( remaining,'remaining-------' ,sick_day,'sick_day-------' ,taken,'taken-------' ,noofday,"noofday--" ,leave_holiday,"leave_holiday--")
                        LeaveDetails.objects.filter(emp_id=i.emp_id).update(remaining=remaining,sick_day=sick_day,taken=taken)
                    else:
                        try:
                            paid_leave_revert=float(i.paid_leaves)
                        except:
                            paid_leave_revert=0
                        paid_leave_revert=paid_leave_revert-leave_holiday
                        try:
                            leave_taken=float(EmpDesk.objects.get(login_id=i.emp_id).leave_taken)
                        except:
                            leave_taken=0
                        leave_taken=leave_taken-paid_leave_revert
                        
                        if leave_taken<0:
                            leave_taken=0
                        try:
                            leave_remaining=float(EmpDesk.objects.get(login_id=i.emp_id).leave_remaining)
                        except:
                            leave_remaining=0
                        leave_remaining=leave_remaining+paid_leave_revert
                        EmpDesk.objects.filter(login_id=i.emp_id).update(leave_taken=leave_taken,leave_remaining=leave_remaining)
                        try:
                            remaining=float(LeaveDetails.objects.get(emp_id=i.emp_id).remaining)
                        except:
                            remaining=0
                        remaining=remaining+paid_leave_revert
                        try:
                            days_allowed=float(LeaveDetails.objects.get(emp_id=i.emp_id).days_allowed)
                        except:
                            days_allowed=0
                        days_allowed=days_allowed+paid_leave_revert
                        try:
                            taken=float(LeaveDetails.objects.get(emp_id=i.emp_id).taken)
                        except:
                            taken=0
                        taken=taken-paid_leave_revert
                        if taken<0:
                            taken=0
                        print( remaining,'remaining-------' ,days_allowed,'days_allowed-------', taken,'taken-------',noofday,"noofday--" ,leave_holiday,"leave_holiday--")
                        LeaveDetails.objects.filter(emp_id=i.emp_id).update(remaining=remaining,days_allowed=days_allowed,taken=taken)

             
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
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                except:
                    pass
            
            else:
                emp=EmpLeaves.objects.filter(id=empid)
                date_l = date.today()
                for e in emp:
                    pass
                    
                  
                

        
        sl=[]
        pl=[]
        leave=[]
        user_types = ['3', '2']
        leaves_detail = EmpLeaves.objects.filter(user_type__in=user_types, hr_id=request.session['id']).order_by('id')
        
        leave_details=LeaveDetails.objects.filter(emp_id=request.session['id']).order_by('id')
        for i in leaves_detail:
            detail=LeaveDetails.objects.filter(emp_id=i.emp_id)
            sl.append(detail[0].sick_day)
            pl.append(detail[0].days_allowed)
            leave.append(i)
        # leaves_detail = zip(leaves_detail,leave_details)
     
        leave.reverse()
        sl.reverse()
        pl.reverse()
        remaining=leave_details[0].remaining
      

        taken=leave_details[0].taken
        leaves=zip(sl,pl,leave)
        name=request.session['name']
        try:
            sl=LeaveDetails.objects.get(emp_id=request.session['id']).sick_day
        except:
            sl=0
        try:
            pl=LeaveDetails.objects.get(emp_id=request.session['id']).days_allowed
        except:
            pl=0
        emp_leaves=EmpLeaves.objects.filter(emp_id=request.session['id']).order_by('-id')
        print(sl,pl)
        return render(request,'HR_leave.html',{'emp_leaves':emp_leaves,'remaining_leaves':remaining_leaves,'name':name,'leaves_detail':leaves,'remaining':remaining,'taken':taken,'sl':sl,'pl':pl })
    else:
        response=HttpResponseRedirect('../../')
        return response
def HR_profile(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        profileData = EmpDesk.objects.filter(login_id=request.session['id'])
        profileData = profileData[0]

        name=request.session['name']
        return render(request,'HR_profile.html',{'name':name, 'profileData':profileData})
    else:
        response=HttpResponseRedirect('../../')
        return response

def HR_team(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
    
        if request.method=='POST':
            if 'addEmp' in request.POST:
                project=request.POST.get('project')
                employee_name=request.POST.get('employee')
                # employee_name=employee_name.split(' ')

                print(project,'vlogs')
                manager_selected=request.POST.get('manager')
                teams=ProjectDetails.objects.filter(project_name=project)
                team='Team'+str(teams[0].id)

                emp_id=employee_name
                


                designation=EmpDesk.objects.filter(login_id=emp_id)
                managers=ProjectDetails.objects.filter(project_name=project)
                designations=designation[0].designations
                
                manager=managers[0].manager
                employee_name=Login.objects.get(id=emp_id).user_name
                employee_f_name=Login.objects.get(id=emp_id).f_name
                employee_l_name=Login.objects.get(id=emp_id).l_name
                manager_id=EmpDesk.objects.get(login_id=emp_id).manager_id
                hr_id=EmpDesk.objects.get(login_id=emp_id).hr_id

                enployee_names=employee_f_name+' '+employee_l_name

                
                obj=Project_team.objects.filter(project=project,employee_name=employee_name,designation=designations)
                
                if len(obj)>0:
                    pass
    
                else:
                    teams=ProjectDetails.objects.filter(project_name=project)
                    
                    team=teams[0].team
                    print(team)
                    
                    a=Project_team(project=project,team=team,employee_id=emp_id,employee_name=employee_name,manager=manager_selected,designation=designations,crt_date=datetime.now().date(),hr_id=request.session['id'])
                    a.save()
                    start_date,end_date=weekdates()
                    employeedata=Empdata(emp_id=emp_id,status=0,mon=0,tue=0,wed=0,thu=0,fri=0,sat=0,sun=0,total=0,totals=0, start=start_date,end=end_date,project_name=project,
                                         name=enployee_names,statushr=0,date_created=datetime.now(),hr_id=hr_id,manager_id=manager_id)
                    employeedata.save()
            elif 'remove' in request.POST:
                remove_id=request.POST.get('remove')
                remove=Project_team.objects.filter(employee_id=remove_id)
                remove.delete()
                
        managers=Manager.objects.all()
        
        projects=ProjectDetails.objects.filter(hr_id=request.session['id'])
        
            
        team=Project_team.objects.filter(hr_id=request.session['id'])
        name=request.session['name']
        employees=EmpDesk.objects.filter(emp_type='3')
        
                
            
        
        return render(request,'HR_team.html',{'name':name,'team':team,'employees':employees,'managers':managers,"projects":projects})
    else:
        response=HttpResponseRedirect('../../')
        return response
    
def HR_projects(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        
        managers=Manager.objects.all()
   
        if request.method=='POST':
            project=request.POST.get('project')
            client=request.POST.get('client')
            date=request.POST.get('date')
            manager=request.POST.get('manager')
            print(manager)
            managerss=Manager.objects.get(emp_id=manager).name

            if 'add' in request.POST:
                a=ProjectDetails(project_name=project,client_name=client,manager_id=manager,start_date=date,status='PENDING',manager=managerss,crt_date=datetime.now().date(),hr_id=request.session['id'])
                a.save()

            name=request.session['name']
            project=ProjectDetails.objects.filter(hr_id=request.session['id'])
            return render(request,'HR_projects.html',{'name':name,'project':project,'managers':managers})

        project=ProjectDetails.objects.filter(hr_id=request.session['id'])   
        name=request.session['name']
        return render(request,'HR_projects.html',{'name':name,'project':project,'managers':managers})
    else:
        response=HttpResponseRedirect('../../')
        return response

def HR_empTracker(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        name=request.session['name']
        return render(request,'HR_empTracker.html',{'name':name})

    else:
        response=HttpResponseRedirect('../../')
        return response

def HR_editEmp(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        
        
        if request.method=='POST':
            f_name=request.POST.get('fname')
            l_name=request.POST.get('lname')
            mailid=request.POST.get('mailId')
            dob=request.POST.get('DOB')
            # dob='Sep. 05, 2023'
            print(f'--{dob}--')

            try:
                dob = datetime.strptime(dob, '%Y-%m-%d')
                dob = dob.strftime('%Y-%m-%d')  
            except:
                # dob = datetime.strptime(dob, '%y-%m-%d')
                dob = dob
                 
            # dob = dob.strftime('%Y-%m-%d')
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
                # DOJ = datetime.strptime(DOJ, '%Y-%m-%d')
                DOJ = DOJ
            # DOJ = DOJ.strftime('%Y-%m-%d')
            print(DOJ,dob,'------------------')
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
            HR=request.POST.get('HR')
            Address=request.POST.get('Address')
            if 'cancel_emp' in request.POST:
                return redirect('../../hr/HR_empList')
            if 'edit_emp' in request.POST:
                EmpDesk.objects.filter(login_id = request.session['edit_emp']).update(f_name=f_name,l_name=l_name,gender=gender,
                                                                                      designation=designation,
                                                                                      doj=DOJ,dob=dob,
                                                                                      email=mailid, mobile=phoneNo,
                                                                                      mobile_alt=AltPhoneNo,address=Address,
                                                                                      salary=salary,bank_name=bankName,
                                                                                      account_number=acctNo,ifsc=ifsc_code,
                                                                                      branch=branch,current_project=CurrProject,
                                                                                      team_name=teamName,designations=designation,
                                                                                      managers=manager,hr_id=HR
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
        return render(request,'HR_editEmp.html',{'name':name,'leaveDetails':leaveDetails, 'employee':data,'managers':managers,'manager':manager, 'hr':HR, 'designation':designation})

def HR_Edit_Hr(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="1":
        
        
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
        return render(request,'HR_edit_HR.html',{'name':name,'leaveDetails':leaveDetails, 'employee':data,'managers':managers,'manager':manager, 'hr':HR, 'designation':designation})

def HR_Edit_Manager(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response

    if request.session['user']=="1":
        
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
        return render(request,'HR_edit_Manager.html',{'name':name,'leaveDetails':leaveDetails, 'employee':data,'managers':managers,'manager':manager, 'hr':HR, 'designation':designation})


def HR_attendance(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    empdetails=Login.objects.exclude(Q(activation='Deactive')|Q(user_type='4')) 
    for i in empdetails:
        try:
            user=i.user_name
            print(user,i.id,1)
            try:
                hr_id=EmpDesk.objects.get(login_id=i.id).hr_id
            except:
                hr_id= request.session['id']
            session_hr_id=request.session['id']
            session_hr_id=str(session_hr_id)
            if hr_id == session_hr_id:
                print('welcome')
                name=str(i.f_name)+' '+str(i.l_name)
                user=i.user_name
                print(user)
                month=date.today().month
                year=date.today().year
                if month<12:
                    next_month=month+1
                    next_year=year
                else:
                    next_month=1
                    next_year=year+1
                
                today=date.today()
                attendance_obj=Attendance.objects.filter(user=user,month=month,year=year,hr_id=hr_id)
                # print(attendance_obj,'licid')
                if len(attendance_obj)<1:
                    Attendance.objects.create(user=user,name=name,month=month,year=year,hr_id=hr_id)
                    
                attendance_obj=Attendance.objects.filter(user=user,month=next_month,year=next_year,hr_id=hr_id)
                if len(attendance_obj)<1:
                    Attendance.objects.create(user=user,name=name,month=next_month,year=year,hr_id=hr_id)
        except:
            pass
    month=date.today().month
    year=date.today().year  

    Emp_Leaves=EmpLeaves.objects.annotate(start_date=Cast('from_dt', output_field=DateField()),
                                          end_date=Cast('to_dt', output_field=DateField())).filter(
                                          start_date__month=month,start_date__year=year,status='Approved')
    print(Emp_Leaves,month ,year,'[[[[[[[[[[]]]]]]]]]]')
    attendance=Attendance.objects.filter(month=month,year=year)
    day=date.today().day
    day='day'+str(day)
    for i in attendance:
        # print(i.user,'Hells')
        days={'day1':i.day1,'day2':i.day2,'day3':i.day3,'day4':i.day4,'day5':i.day5,'day6':i.day6,'day7':i.day7,'day8':i.day8,'day9':i.day9,'day10':i.day10,'day11':i.day11,'day12':i.day12,'day13':i.day13,'day14':i.day14,'day15':i.day15,'day16':i.day16,'day17':i.day17,'day18':i.day18,'day19':i.day19,'day20':i.day20,'day21':i.day21,'day22':i.day22,'day23':i.day23,'day24':i.day24,'day25':i.day25,'day26':i.day26,'day27':i.day27,'day28':i.day28,'day29':i.day29,'day30':i.day30,'day31':i.day31}  
        if days[f'{day}']==None:
        
            try:
                activation = Login.objects.get(user_name=i.user).activation
          
                if activation=='Deactive':
                    Attendance.objects.filter(user=i.user,month=month,year=year).update(**{day: 'D'})
                elif activation=='Active':
                    Attendance.objects.filter(user=i.user,month=month,year=year).update(**{day: 'P'})
            except:
                pass
    for i in Emp_Leaves:
        all_dates = get_dates(i.start_date, i.end_date)
        print(all_dates,'all_dates------******************')
        try:
            user = Login.objects.get(id=i.emp_id).user_name
        except:
            user=''
        pl=i.paid_leaves
        pl=float(pl)
        leave_flag=0
        for j in  all_dates:
            day=j.day
            leave_month=j.month
            leave_year=j.year
            day='day'+str(day)
            if pl> leave_flag:
                dats=Attendance.objects.filter(Q(user=user,month=leave_month,year=leave_year,**{day: 'PL'})|Q(user=user,month=leave_month,year=leave_year,**{day: 'SL'}))
                
                if len(dats)==0:
                    if i.leave_type =='Sick Leave':
                        Attendance.objects.filter(user=user,month=leave_month,year=leave_year).update(**{day: 'SL'})
                    else:
                        Attendance.objects.filter(user=user,month=leave_month,year=leave_year).update(**{day: 'PL'})

            else:
                dats=Attendance.objects.filter(user=user,month=leave_month,year=leave_year,**{day: 'UL'})
                if len(dats)==0:
                    Attendance.objects.filter(user=user,month=leave_month,year=leave_year).update(**{day: 'UL'})
            dats=Attendance.objects.filter(user=user,month=leave_month,year=leave_year,**{day: 'UL'})
           
    holidays= get_sundays_and_saturdays_current_month()
    for i in holidays:
        day='day'+str(i)
        dats=Attendance.objects.filter(user=user,month=month,year=year,**{day: 'HL'})
        if len(dats)==0:
            Attendance.objects.filter(month=month,year=year).update(**{day: 'HL'})
       
    if request.method=='POST':
        month=request.POST.get('month')
        year=request.POST.get('year')
        try:
            month=int(month)
            year=int(year)
        except:
            pass
        
        if 'absent' in request.POST:
            absent=request.POST.get('absent')
            absent=absent.split(',')
           
            user=absent[0]
            day=absent[-1]
            day='day'+str(day)
            Attendance.objects.filter(user=user,month=month,year=year).update(**{day: 'A'})
        elif 'halfday' in request.POST:
            halfday=request.POST.get('halfday')
            halfday=halfday.split(',')
            user=halfday[0]
            day=halfday[-1]
            day='day'+str(day)
            Attendance.objects.filter(user=user,month=month,year=year).update(**{day: 'HF'})
        elif 'holiday' in request.POST:
            holiday=request.POST.get('holiday')
            holiday=holiday.split(',')
            user=holiday[0]
            day=holiday[-1]
            day='day'+str(day)
            Attendance.objects.filter(user=user,month=month,year=year).update(**{day: 'HL'})
        elif 'next' in request.POST:
            if month==12:
                month=1
                year=year+1
            else:
                month=month+1
        elif 'prev' in request.POST:
            if month==1:
                month=12
                year=year-1
            else:
                month=month-1
        # return HttpResponse() 
   

    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        leapyear=1
    else:
        leapyear=0
    attendance_obj=Attendance.objects.filter(month=month,year=year,hr_id=request.session['id'])     
    
    return render(request,'HR_attendance.html',{'attendance':attendance_obj,'month':month,'leapyear':leapyear,'year':year})

def HR_payment_payroll(request): 
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    empdetails=EmpDesk.objects.exclude(Q(emp_type='4')|Q(emp_type='2')|Q(activation='Deactive')).filter(hr_id=request.session['id'])
    main_start_time= datetime.now()
    month=date.today().month
    year=date.today().year
    if request.method=='POST':
        if 'prev' in request.POST:
            month=month-1
            if month==0:
                month=12
                year=year-1
        if 'next' in request.POST:
            month=month+1
            if month==13:
                month=1
                year=year+1
    
    for i in  empdetails:
        name=str(i.f_name)+' '+str(i.l_name)
        user=Login.objects.get(id=i.login_id).user_name
        

        salary = i.salary
        # print(salary)

        payroll_obj=Payroll.objects.filter(user_name=user,month=month,year=year,hr_id=request.session['id'])
        if len(payroll_obj)<1:
            Payroll.objects.create(user_name=user,employee=name,month=month,year=year,salary_per_month=salary,paid=0,hr_id=request.session['id'])
        salary=int(salary)
        salary_pd = salary/30
        abscent=0
        paid = 0
        paid_vacation_day = 0
        unpaid_vacation_day = 0
        sick_leaves=0
        halfdays=0
        internet_charges=0
        start_time= datetime.now()
        
        for i in range(1,32):
            
            if len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'H'}))>0:
                paid+=1
            elif len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'PL'}))>0:
                paid_vacation_day+=1
            elif len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'UL'}))>0:
                unpaid_vacation_day+=1
            elif len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'SL'}))>0:
                sick_leaves+=1
            elif len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'HF'}))>0:
                halfdays+=1
            elif len(Attendance.objects.filter(user=user,month=month,year=year,**{f'day{i}':'A'}))>0:
                abscent+=1
        paid_holiday_rs=paid*salary_pd   
        paid_vacation=paid_vacation_day*salary_pd
        unpaid_vacation=unpaid_vacation_day*salary_pd
        sick_leave=sick_leaves*salary_pd
        halfday=(halfdays*salary_pd)/2
        unpaid_vacation_day=unpaid_vacation_day+abscent
        abscent_rs=abscent*salary_pd
        unpaid_vacation=unpaid_vacation+abscent_rs
        print(name,'name','--',salary,'salary','--',unpaid_vacation,'unpaid_vacation','--',abscent_rs,'abscent_rs')
        salary_paid=salary-unpaid_vacation+internet_charges #-abscent_rs
        if salary_paid<0:
            salary_paid=0
        # print('paid_holiday_rs',paid_holiday_rs,'paid_vacation',paid_vacation,'unpaid_vacation',unpaid_vacation,'sick_leave',sick_leave,'halfday',halfday,'unpaid_vacation_day',unpaid_vacation_day,'abscent_rs',abscent_rs,'unpaid_vacation',unpaid_vacation,'salary_paid',salary_paid)
        Payroll.objects.filter(user_name=user,month=month,year=year,paid='0').update(paid_holiday=paid,paid_holiday_rs=paid_holiday_rs,
        paid_vacation_day=paid_vacation_day,paid_vacation_day_rs=paid_vacation,unpaid_vacation=unpaid_vacation_day,
        unpaid_vacation_rs=unpaid_vacation,paid_sick_leave=sick_leaves,paid_sick_leave_rs=sick_leave,
        internet_charges_rs=internet_charges,salary_and_other_charges_rs=salary_paid,paid_to_employee=salary_paid)

        end_time= datetime.now()
        time_difference = end_time - start_time
        # print('inner-loop-Time difference:', time_difference)
      
    main_end_time= datetime.now()
    time_difference2 = main_end_time - main_start_time
    print('main-loop-Time difference:', time_difference2)        
    payroll_obj = Payroll.objects.filter(month=month, year=year,hr_id=request.session['id'])
    return render(request, 'HR_payment_payroll.html',{'month':month, 'year':year, 'payroll':payroll_obj})

def get_sundays_and_saturdays_current_month():
    today = date.today()
    start_date = date(today.year, today.month, 1)
    end_date = start_date + timedelta(days=31) 
    while end_date.month !=start_date.month:
        end_date=end_date - timedelta(days=1)
    
    sundays = []
    saturdays = []

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 6:  # Sunday is the 6th day of the week
            sundays.append(current_date.day)
        elif current_date.weekday() == 5:  # Saturday is the 5th day of the week
            saturdays.append(current_date.day)
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
    return holiday

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


def attendance_test(request):
      
    
    return render(request,'attendance_test.html')
def attendance_test_create(request):
  
    attendance=request.POST.get('absent')
    
    attendance=attendance.split(',')
    
    Attendance.objects.filter(user=attendance[0],month=attendance[3],year=attendance[4]).update(**{attendance[1]: attendance[2]})
    attendance_obj=Attendance.objects.filter(month=attendance[3],year=attendance[4])
    return HttpResponse({'attendance':attendance_obj}) 


def HR_payroll(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    print('hello vlog')
    paid=request.POST.get('paid')
    paid=paid.split(',')
    print(paid)
    Payroll.objects.filter(user_name=paid[0],month=paid[1],year=paid[2]).update(paid=paid[3])
    return HttpResponse({'success':paid}) 

def leave_test(request):
    return render(request, 'leave_test.html')
from django.http import JsonResponse
def filter_data(request):
    # selected_hr_id = request.GET.get('hr_id')
    selected_manager_id = request.GET.get('managerid')
    manager_id=Manager.objects.get(name=selected_manager_id).emp_id
    print('hlo vlog welcome to my guys')
    print(selected_manager_id)
    
    # managers = Manager.objects.filter(hr_id=selected_hr_id)
    projects = ProjectDetails.objects.filter(manager_id=manager_id)
    employees=EmpDesk.objects.filter(manager_id=manager_id)
    
    # manager_list = [{'id': manager.emp_id, 'name': manager.name} for manager in managers]
    project_list = [{'id': project.id, 'name': project.project_name} for project in projects]
    employee_list = [{'id': employee.login_id, 'name': str(employee.f_name)+" " +str(employee.l_name) } for employee in employees]
    print(project_list)
    print(employee_list)
    
    data = {
        # 'managers': manager_list,
        'projects': project_list,
        'employees': employee_list
    }
    
    return JsonResponse(data)
def filter_data_add_emp(request):
    selected_hr_id = request.GET.get('hr_id')
    selected_manager_id = request.GET.get('managerid')
    
    
    print('hlo vlog welcome to my guys')
    print(selected_hr_id,selected_manager_id)
    try:
        manager_id= Manager.objects.get(name=selected_manager_id).emp_id
    except:
        manager_id=0   
    
    managers = Manager.objects.filter(hr_id=selected_hr_id)
    projects = ProjectDetails.objects.filter(manager_id=selected_manager_id)
    
        
    print(managers)
    manager_list = [{'id': manager.emp_id, 'name': manager.name} for manager in managers]
    project_list = [{'id': project.id, 'name': project.project_name} for project in projects]
   

    data = {
        'managers': manager_list,
        'projects': project_list
        
    }
    print(data)
    return JsonResponse(data)
def add_to_project_team(request,manager,CurrProject,name, emp_id,designation):
    print(request,manager,CurrProject,name, emp_id,designation)
    if CurrProject== '0' or CurrProject== '' or CurrProject== 'None' or CurrProject== None:
        pass
    else:
        Projectteam=Project_team.objects.filter(project=CurrProject, manager=manager, employee_id=emp_id)
        if len(Projectteam)>0:
            pass
        else:
            try:
                team=Project_team.objects.get(project=CurrProject).team
            except:
                team='Team'   
            if len(Project_team.objects.filter( project=CurrProject, team=team, manager=manager, employee_name=name, employee_id=emp_id, designation=designation,hr_id=request.session['id']))>0:
                pass
            else:
                Project_team.objects.create( project=CurrProject, team=team, manager=manager, employee_name=name, employee_id=emp_id, designation=designation, crt_date=date.today(),hr_id=request.session['id'])
    
def HR_empTracker_Details(request):
    try:
        if request.session['user']=="1":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response  
    except:  
        response=HttpResponseRedirect('../../')
        return response
    start_date_str = request.session['start_dt']
    print(f'-----------{start_date_str}--------------start_date_str-------------------------')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    start_date=start_date.strftime('%Y-%m-%d')
    empdesk=EmpDesk.objects.filter(login_id=request.session['approved_emp_id'])
    
    try:
        empdesk=empdesk[0]
    except:
        pass
    
    try:
        img=Login.objects.get(id=request.session['approved_emp_id']).image
        
    except:
        img=''
    data=Empdata.objects.filter(emp_id=request.session['approved_emp_id'],start=start_date)
   
    try:
        comments=Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).employee_comment
        tue_comm = Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).emp_comm_tue
        wed_comm = Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).emp_comm_wed
        thu_comm = Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).emp_comm_thu
        fri_comm = Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).emp_comm_fri
        sat_comm = Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).emp_comm_sat
        print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'try')
    except:
        comments = ''
        tue_comm = ''
        wed_comm = ''
        thu_comm = ''
        fri_comm = ''
        sat_comm = ''
    return render(request, 'HR_empTracker_Details.html',{'comments':comments,'data':data,'empdesk':empdesk,'img':img,
    'tue_comm':tue_comm,'wed_comm':wed_comm,'thu_comm':thu_comm,'fri_comm':fri_comm,'sat_comm':sat_comm})  

def manage_attendance(request,i):
        all_dates = get_dates(i.from_dt, i.to_dt)
        print(all_dates,'all_dates------******************')
        try:
            user = Login.objects.get(id=i.emp_id).user_name
        except:
            user=''
        pl=i.paid_leaves
        pl=float(pl)
        leave_flag=0
        for j in  all_dates:
            day=j.day
            leave_month=j.month
            leave_year=j.year
            day='day'+str(day)

            att=Attendance.objects.filter(user=user,month=leave_month,year=leave_year,).values().first()
           
            if att[day]  == 'PL' or att[day]  == 'UL'  or att[day]  == 'SL':
                Attendance.objects.filter(user=user,month=leave_month,year=leave_year).update(**{day: ''})
           
            
       

        return 0


def payroll_emp(request):
    return render(request,'payroll_emp.html')
























    